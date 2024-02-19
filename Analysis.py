import matplotlib.pyplot as plt
import yaml
import requests
import logging
import subprocess
import statistics

class Analysis():

    def __init__(self) -> None:
        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']

        # initialize empty dictionary to hold the configuration
        config = {}

        # load each config file and update the config dictionary
        for path in CONFIG_PATHS:
            with open(path, 'r') as f:
                this_config = yaml.safe_load(f)
            config.update(this_config)

        self.config = config       
        
    def load_data(self) -> None:
        ''' Retrieve data from the Spotify API
        This function makes an HTTPS request to the Spotify API and retrieves Artist Name Lil and the popularity of this name. 
        The data is stored in the Analysis object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        '''    
        CLIENT_ID = self.config['spotify_client_id']
        CLIENT_SECRET = self.config['spotify_client_secret']
        AUTH_URL = 'https://accounts.spotify.com/api/token'

        auth_response = requests.post(AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })
        auth_response_data = auth_response.json()
        access_token = auth_response_data['access_token']
        headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
        
        try:
            data = requests.get('https://api.spotify.com/v1/search?query=jeni&type=artist&limit=50&market=CA' , headers=headers).json()
            self.data = data            
            logging.info(f'Data Loaded Successfully from Spotify')
        except Exception as e:
            logging.error('Error loading Data from Spotify', exc_info=e)
            raise e.add_note('Please enter a valid spotify path.')
    
      
    def compute_analysis(self) -> int:
        '''Analyze previously-loaded data.
        This function runs an analytical measure mean
        and returns an integer.

        Parameters
        ----------
        None

        Returns
        -------
        analysis_output : int

        '''
        jeni_artists = self.data['artists']['items'] 
        name_list = []
        pop_list = []
        for artist in jeni_artists:
            name_list.append(artist['name'])
            pop_list.append(artist['popularity'])
        
        self.name_list = name_list
        self.pop_list = pop_list
        
        if pop_list:  # Check if pop_list is not empty
            return statistics.mean(pop_list)
        else:
            return 0.0  # Return a default value if pop_list is empty
        
    def plot_data(self, save_path = "output_plot.png") -> plt.Figure:
        plt.plot(self.name_list[:10], self.pop_list[:10])
        plt.xticks(rotation=45, ha='right')
        plt.xlabel(self.config['x_label'])
        plt.ylabel(self.config['y_label'])
        plt.title(self.config['title'])
        #plt.show()
        plt.savefig(save_path)
        
    def notify_done(self, message: str) -> None:
        command = ['ntfy', '-b', 'webpush', 'send', message]
        if message:
            command.extend(['-t', message])
        subprocess.run(command)
    