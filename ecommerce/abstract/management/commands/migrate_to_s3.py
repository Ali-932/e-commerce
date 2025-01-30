import os
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from django.conf import settings
import boto3
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig


class Command(BaseCommand):
    help = 'Parallel S3 media uploads with progress tracking'

    def add_arguments(self, parser):
        parser.add_argument('--bucket', type=str, required=True)
        parser.add_argument('--prefix', type=str, default='media')
        parser.add_argument('--progress-file', default='s3_upload_progress.json')
        parser.add_argument('--workers', type=int, default=10,
                            help='Number of parallel upload threads')
        parser.add_argument('--multipart-size', type=int, default=50,
                            help='Multipart threshold in MB')

    def handle(self, *args, **options):
        self.s3 = boto3.client('s3',
                               aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                               region_name=settings.AWS_REGION)

        self.bucket_name = options['bucket']
        self.prefix = options['prefix']
        self.progress_file = options['progress_file']
        self.workers = options['workers']
        self.lock = threading.Lock()

        # Shared progress state
        self.uploaded_files = self.load_progress()
        print(len(self.uploaded_files))
        self.media_root = settings.MEDIA_ROOT
        print('starting')
        # Configure parallel uploads
        transfer_config = TransferConfig(
            multipart_threshold=options['multipart_size'] * 1024 * 1024,
            max_concurrency=self.workers
        )

        # Collect all files first for accurate progress tracking
        file_queue = self.get_upload_queue()
        print(f'to queue {len(file_queue)}')
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = []
            for local_path, s3_key in file_queue:
                futures.append(executor.submit(
                    self.upload_file,
                    local_path,
                    s3_key,
                    transfer_config
                ))

            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    self.stderr.write(str(e))

    def get_upload_queue(self):
        queue = []
        num_of_uploaded = 0
        for root, _, files in os.walk(self.media_root):
            if 'cache' in root.split(os.sep):
                continue
            for filename in files:
                local_path = os.path.join(root, filename)
                relative_path = os.path.relpath(local_path, self.media_root)
                s3_key = os.path.join(self.prefix, relative_path).replace('\\', '/')
                print(s3_key)
                if s3_key not in self.uploaded_files:
                    queue.append((local_path, s3_key))
                else:
                    num_of_uploaded+=1
        print(num_of_uploaded)
        return queue

    def upload_file(self, local_path, s3_key, transfer_config):
        try:
            self.s3.upload_file(
                Filename=local_path,
                Bucket=self.bucket_name,
                Key=s3_key,
                Config=transfer_config,
                ExtraArgs={'ContentType': self.get_content_type(local_path)}
            )
            self.stdout.write(f'Uploaded {local_path} to s3://{s3_key}')

            with self.lock:
                self.uploaded_files.add(s3_key)
                self.save_progress()
                self.stdout.write(f'Uploaded {s3_key}')

        except ClientError as e:
            self.stderr.write(f'Failed {s3_key}: {e}')

    def load_progress(self):
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                return set(json.load(f))
        return set()

    def save_progress(self):
        with open(self.progress_file, 'w') as f:
            print('saving progress')
            json.dump(sorted(self.uploaded_files), f, indent=2)


    def get_content_type(self, filename):
        # Add more MIME types as needed
        return {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.mp4': 'video/mp4',
            '.mov': 'video/quicktime',
        }.get(os.path.splitext(filename)[1].lower(), 'binary/octet-stream')