import os
import sys
import requests
from tqdm import tqdm


class Downloader:
    def __init__(self, model):
        self.subdir = os.path.join('models', model)
        if not os.path.exists(self.subdir):
            os.makedirs(self.subdir)
            self.subdir = self.subdir.replace('\\','/') # needed for Windows
    def __iter__(self):
        return iter(['checkpoint','encoder.json','hparams.json','model.ckpt.data-00000-of-00001', 'model.ckpt.index', 'model.ckpt.meta', 'vocab.bpe'])
    
    def download(self):

        for filename in self:
            r = requests.get("https://storage.googleapis.com/gpt-2/" + self.subdir + "/" + filename, stream=True)

            with open(os.path.join(self.subdir, filename), 'wb') as f:
                file_size = int(r.headers["content-length"])
                chunk_size = 1000
                with tqdm(ncols=100, desc="Fetching " + filename, total=file_size, unit_scale=True) as pbar:
                    # 1k for chunk_size, since Ethernet packet size is around 1500 bytes
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
                        pbar.update(chunk_size)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('You must enter the model name as a parameter, e.g.: download_model.py 124M')
        sys.exit(1)

    model = sys.argv[1]
    Downloader(model).download()

