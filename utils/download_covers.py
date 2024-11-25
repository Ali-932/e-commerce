import dotenv
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import argparse
from tqdm import tqdm
dotenv.load_dotenv()

from sqlalchemy import create_engine, MetaData, text

engine = create_engine(
    "postgresql://{}:{}@{}:{}/{}".format(
        dotenv.get_key(".env", "DB_USER"),
        dotenv.get_key(".env", "DB_PASS"),
        dotenv.get_key(".env", "DB_HOST"),
        dotenv.get_key(".env", "DB_PORT"),
        dotenv.get_key(".env", "DB_NAME"),
    )
)
conn = engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)


def get_cover_lists():
    with engine.connect() as connection:
        result = connection.execute(text("select id,image from product_item where image LIKE '%mangadex%';"))
        rows = result.fetchall()
    text_rows = [{"id": row[0], "image": row[1]} for row in rows]
    # text_rows = [row[0] for row in rows]
    return text_rows


url_list = get_cover_lists()


def download_image(session, url, output_dir, image_id):
  try:
      response = session.get(url, timeout=30)
      response.raise_for_status()
      filename = f"{image_id}"
      if not os.path.splitext(filename)[1]:
          # Try to get from Content-Type
          content_type = response.headers.get('Content-Type')
          if content_type:
              ext = content_type.split('/')[-1]
              filename += f".{ext}"
          else:
              filename += ".jpg"  # Default extension

      filepath = os.path.join(output_dir, filename)

      with open(filepath, 'wb') as f:
          f.write(response.content)
      return True, url
  except Exception as e:
      return False, url

def create_output_directory(base_dir):
  if not os.path.exists(base_dir):
      os.makedirs(base_dir)

def main(output_dir, batch_size, max_workers):
  create_output_directory(output_dir)
  urls_with_id = get_cover_lists()
  total = len(urls_with_id)
  print(f"Total URLs to download: {total}")

  failed_downloads = []

  # Create a requests session for connection pooling
  with requests.Session() as session:
      # Iterate over the URLs in batches
      for batch_start in range(0, total, batch_size):
          batch_end = min(batch_start + batch_size, total)
          batch = urls_with_id[batch_start:batch_end]
          with ThreadPoolExecutor(max_workers=max_workers) as executor:
              # Prepare future tasks
              futures = {
                  executor.submit(download_image, session, dict_object['image'], output_dir, dict_object['id']): dict_object['image']
                  for dict_object in batch
              }

              # Use tqdm to display progress bar for the current batch
              for future in tqdm(as_completed(futures), total=len(futures),
                                 desc=f"Downloading batch {batch_start // batch_size + 1}"):
                  success, url = future.result()
                  if not success:
                      failed_downloads.append(url)

  # Summary
  print("\nDownload complete.")
  print(f"Successfully downloaded {total - len(failed_downloads)} images.")
  if failed_downloads:
      print(f"Failed to download {len(failed_downloads)} images. Check 'failed_downloads.txt' for details.")
      with open('failed_downloads.txt', 'w') as f:
          for url in failed_downloads:
              f.write(url + '\n')

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Download images from a list of URLs in batches.")
  parser.add_argument('-o', '--output', default='downloaded_images', help='Directory to save downloaded images.')
  parser.add_argument('-b', '--batch', type=int, default=100, help='Number of images to download per batch.')
  parser.add_argument('-w', '--workers', type=int, default=10, help='Number of concurrent download threads.')

  args = parser.parse_args()
  main(args.output, args.batch, args.workers)
