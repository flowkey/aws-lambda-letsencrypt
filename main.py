import os
from certbot import main as app


def handler(event, context):
    domains = os.getenv('DOMAINS')
    email = os.getenv('EMAIL')
    distribution_id = os.getenv('DISTRIBUTION_ID')
    workdir = os.getenv('WORKDIR') or '/tmp/letsencrypt'
    test_flag = os.getenv('TEST_MODE')

    args = [
        '-i', 'certbot-s3website:installer', '-a', 'certbot-s3website:auth',
        '-d', domains, '--agree-tos', '--text', '--email', email,
        '--config-dir', workdir, '--logs-dir', workdir, '--work-dir', workdir,
        '--certbot-s3website:installer-cf-distribution-id', distribution_id,
        '--keep'
    ]
    if test_flag:
        args.append('--staging')

    app.main(args)
