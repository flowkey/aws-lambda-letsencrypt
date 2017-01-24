import os
import logging

import zope.interface

from certbot import interfaces
from certbot.plugins import common

from acme import challenges

import boto3
from botocore.exceptions import ClientError

from OpenSSL import crypto


logger = logging.getLogger(__name__)

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(common.Plugin):
    """S3 Website Authenticator."""

    description = "S3 Website Authenticator plugin"

    def prepare(self):
        pass

    def more_info(self):
        pass

    def get_chall_pref(self, domain):
        return [challenges.HTTP01]

    def perform(self, achalls):
        responses = []
        for achall in achalls:
            responses.append(self._perform_single(achall))
        return responses

    def _perform_single(self, achall):
        response, validation = achall.response_and_validation()

        key = achall.chall.path[1:]
        logger.info("challenge token storing: {} -> {}".format(key, validation))

        s3 = boto3.resource('s3')
        s3.Bucket(achall.domain).put_object(
            Key=key,
            Body=validation,
            ACL='public-read'
        )

        if response.simple_verify(
            achall.chall, achall.domain,
            achall.account_key.public_key(), self.config.http01_port):
            return response
        else:
            logger.error(
                "Self-verify of challenge failed, authorization abandoned!")
            return None

    def cleanup(self, achalls):
        for achall in achalls:
            self._cleanup_single(achall)

    def _cleanup_single(self, achall):
        key = achall.chall.path[1:]
        logger.info("challenge token removing: {}".format(key))

        s3 = boto3.resource('s3')
        s3.Bucket(achall.domain).Object(key).delete()

@zope.interface.implementer(interfaces.IInstaller)
@zope.interface.provider(interfaces.IPluginFactory)
class Installer(common.Plugin):
    """IAM+CloudFront Installer."""

    @classmethod
    def add_parser_arguments(cls, add):
        add("cf-distribution-id", default=os.getenv('CF_DISTRIBUTION_ID'),
            help="CloudFront distribution id")

    description = "IAM+CloudFront Installer plugin"

    def prepare(self):
        pass

    def more_info(self):
        pass

    def get_all_names(self):
        pass

    def deploy_cert(self, domain, cert_path, key_path, chain_path, fullchain_path):
        if self.config.rsa_key_size > 2048:
            logger.error("The maximum key size allowed for CloudFront is 2048")
            return

        logger.info("deploying certificate for {}".format(domain))

        iam = boto3.client('iam')
        cloudfront = boto3.client('cloudfront')

        body = open(cert_path).read()
        key = open(key_path).read()
        chain = open(chain_path).read()
        body_parsed = crypto.load_certificate(crypto.FILETYPE_PEM, body)
        name = "{}-{}".format(
            body_parsed.get_subject().commonName,
            body_parsed.get_notBefore()
        )

        # check current registered certificate
        current = None
        try:
            response = iam.get_server_certificate(ServerCertificateName=name)
            current = crypto.load_certificate(
                crypto.FILETYPE_PEM,
                response['ServerCertificate']['CertificateBody']
            )
        except ClientError:
            pass

        if current and current.digest('sha256') == body_parsed.digest('sha256'):
            logger.info("server certificate {} already registered, skip".format(name))
            return

        # upload certificate
        response = iam.upload_server_certificate(
            Path="/cloudfront/",
            ServerCertificateName=name,
            CertificateBody=body,
            PrivateKey=key,
            CertificateChain=chain
        )
        cert_id = response['ServerCertificateMetadata']['ServerCertificateId']

        # get current CloudFront configuration
        distribution_id = self.conf('cf-distribution-id')
        response = cloudfront.get_distribution_config(Id=distribution_id)
        dist_cfg = response['DistributionConfig']
        etag = response['ETag']
        cert_cfg = dist_cfg['ViewerCertificate']

        cert_cfg['IAMCertificateId'] = cert_id
        cert_cfg['Certificate'] = cert_id

        response = cloudfront.update_distribution(
            DistributionConfig=dist_cfg,
            Id=distribution_id,
            IfMatch=etag
        )

    def enhance(self, domain, enhancement, options=None):
        pass

    def supported_enhancements(self):
        return []

    def save(self, title=None, temporary=False):
        pass

    def rollback_checkpoints(self, rollback=1):
        pass

    def recovery_routine(self):
        pass

    def view_config_changes(self):
        pass

    def config_test(self):
        pass

    def restart(self):
        pass
