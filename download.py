# Using https://github.com/OneDrive/onedrive-sdk-python
# and https://docs.microsoft.com/en-us/onedrive/developer/rest-api/getting-started/?view=odsp-graph-online to get started with the API
import onedrivesdk
import os
import logging
logging.basicConfig(format='%(levelname)s:\t%(message)s', level=logging.INFO)

root_folder = '/home/user/OneDrive'
folder = ''
current = os.getcwd()
redirect_uri = 'https://login.live.com/oauth20_desktop.srf'
api_base_url='https://api.onedrive.com/v1.0/'
scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

creds = {'EMAIL':
         (
             'SECRET',
             'ID'
         ),
         'EMAIL':
         (
             'SECRET',
             'ID'
         )
        }

# List of only directories in the root folder to download
dir_yes = []
# Global list of directories not to download
dir_no = []
last_id = ''
recovery = False

def first_auth(account):
    client_secret = creds[account][0]
    client_id = creds[account][1]

    http_provider = onedrivesdk.HttpProvider()
    auth_provider = onedrivesdk.AuthProvider(
            http_provider=http_provider,
            client_id=client_id,
            scopes=scopes)

    client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)
    auth_url = client.auth_provider.get_auth_url(redirect_uri)
    print('Paste this URL into your browser, approve the app\'s access.')
    print('Copy everything in the address bar after "code=", and paste it below.')
    print(auth_url)
    code = input('Paste code here: ')

    client.auth_provider.authenticate(code, redirect_uri, client_secret)
    auth_provider.save_session()
    return client

def auth(account):
    client_secret = creds[account][0]
    client_id = creds[account][1]
    http_provider = onedrivesdk.HttpProvider()
    auth_provider = onedrivesdk.AuthProvider(http_provider, client_id, scopes)
    auth_provider.load_session()
    auth_provider.refresh_token()
    client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)
    return client

def download_all(client, item_id='root'):
    global recovery

    folder = client.item(drive='me', id=item_id).children.get()
    for item in folder:
        if (item_id == 'root' and item.name not in dir_yes) or item.name in dir_no:
            continue
        if item.folder:
            if not recovery and not os.path.exists(item.name):
                os.mkdir(item.name)
            os.chdir(item.name)
            download_all(client, item.id)
        else:
            if recovery:
                if item.id != last_id:
                    continue
                else:
                    try:
                        os.remove(item.name)
                    except:
                        pass
                    recovery = False
            open(current+'/last_id','w').write(item.id)
            filename = os.getcwd() + '/' + item.name
            logging.info('Downloading ' + filename.replace(root_folder,' ') + '...')            
            client.item(drive='me', id=item.id).download(filename)

    os.chdir('..')
    return

def setup(client):
    if os.path.exists('last_id'):
        global recovery
        global last_id
        recovery = True
        last_id = open('last_id', 'r').read().strip()
    os.chdir(root_folder)

def main():
    # First authorization with copy/pasting of the token to create the session.pickle
    client = first_auth('EMAIIL')
    # Authorization with the session.pickle
    # client = auth('EMAIL')
    setup(client)
    download_all(client)
    os.chdir(current)
    os.remove('last_id')

if __name__ == '__main__':
    main()

