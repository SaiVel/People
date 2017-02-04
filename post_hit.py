import argparse
import datetime
import os
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price



def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('keys_file')
    parser.add_argument('--production', default=False, action='store_true')
    args = parser.parse_args()


    # read keys
    access_key_id, secret_key = None, None

    with open(args.keys_file, 'r') as keys:
        for line in keys.xreadlines():
            items = [xx.strip() for xx in line.split('=')]
            if items[0] == 'AWSAccessKeyId':
                access_key_id = items[1]
            elif items[0] == 'AWSSecretKey':
                secret_key = items[1]

    if not access_key_id or not secret_key:
        raise RuntimeError('Invalid keys file format.')


    # set up URLs
    if args.production:
        mturk_url = 'mechanicalturk.amazonaws.com'
        preview_url = 'https://www.mturk.com/mturk/preview?groupId='
    else:
        print 'SANDBOX'
        mturk_url = 'mechanicalturk.sandbox.amazonaws.com'
        preview_url = 'https://workersandbox.mturk.com/mturk/preview?groupId='



    # connect
    connection = MTurkConnection(aws_access_key_id=access_key_id,
                                 aws_secret_access_key=secret_key,
                                 host=mturk_url)



    # make the HIT
    question = ExternalQuestion(
        external_url='',                     # URL to serve HIT
        frame_height=600                                          # height of frame
        )

    reward=Price(
        amount=0.05                                               # reward for HIT completion
        )

    create_hit_result = connection.create_hit(
        title='Identify Recognizable People',
        description='Identify the number of recognizable peoplein each image',
        keywords=['identify', 'recognize', 'people', 'images', 'answer', 'count', 'pictures', 'label'],
        max_assignments=10,                                        # number of assignments
        lifetime=datetime.timedelta(days=7),                      # time HIT is available
        duration=datetime.timedelta(minutes=15),                   # time worker has to complete HIT once accepted
        approval_delay=datetime.timedelta(days=3),                # time until HIT is automatically approved
        question=question,
        reward=reward,
        response_groups=('Minimal', 'HITDetail')
        )

    print('Preview: ' + preview_url + create_hit_result[0].HITTypeId)
    print('HIT Id: ' + create_hit_result[0].HITId)




if __name__ == '__main__':
    main()
