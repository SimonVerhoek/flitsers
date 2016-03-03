import dropbox
from credentials import DROPBOX_TOKEN, FILENAME

client = dropbox.client.DropboxClient(DROPBOX_TOKEN)

f = open(FILENAME, 'rb')
response = client.put_file('/{}'.format(FILENAME), f, overwrite=True)

folder_metadata = client.metadata('/')

f, metadata = client.get_file_and_metadata(FILENAME)
out = open(FILENAME, 'wb')
out.write(f.read())
out.close()