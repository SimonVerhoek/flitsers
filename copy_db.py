import os

import dropbox


client = dropbox.client.DropboxClient(os.environ['DROPBOX_TOKEN'])

f = open(os.environ['FILENAME'], 'rb')
response = client.put_file('/{}'.format(os.environ['FILENAME']), f, overwrite=True)

folder_metadata = client.metadata('/')

f, metadata = client.get_file_and_metadata(os.environ['FILENAME'])
out = open(os.environ['FILENAME'], 'wb')
out.write(f.read())
out.close()