import os
from certbot import main as app


def handler(event, context):
    domain = ','.join(os.getenv('DOMAIN').split())
    email = os.getenv('EMAIL')
    distribution_id = os.getenv('DISTRIBUTION_ID')
    workdir = os.getenv('WORKDIR') or '/tmp/letsencrypt'
    test_flag = os.getenv('TEST_MODE')

    args = [
        '-i', 'certbot-s3front:installer', '--dns-route53',
        '-d', domain, '-d', ('*.' + domain),
        '--agree-tos', '--text', '--email', email, '-n',
        '--config-dir', workdir, '--logs-dir', workdir, '--work-dir', workdir,
        '--certbot-s3front:installer-cf-distribution-id', distribution_id,
        '--keep'
    ]
    if test_flag:
        args.append('--staging')

    app.main(args)

if __name__ == "__main__":
    handler(None, None)
