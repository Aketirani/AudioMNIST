import os

import yaml


class Setup:
    """
    The Setup class is used to set up paths
    """

    def __init__(self, cfg_file: str) -> None:
        """
        Initialize the class with the config file, and set up the paths and files

        :param cfg_file: str, name to the config file
        :param cfg_setup: str, name to the config file
        :param src_path: str, path to the audio folder
        :param meta_path: str, path to the meta data folder
        :param data_path: str, path to the data folder
        :param plot_path: str, path to the plots folder
        :param res_path: str, path to the results folder
        :param test_path: str, path to the test folder
        :param model_path: str, path to the model parameters folder
        :param param_path: str, path to the configurations folder
        :param hyperparam_path: str, path to the configurations folder
        """
        self.cfg_file = cfg_file
        self.cfg_setup = self.read_config()
        self.audio_path = self.set_audio_path()
        self.meta_path = self.set_meta_data_path()
        self.data_path = self.set_data_path()
        self.plot_path = self.set_plot_path()
        self.res_path = self.set_result_path()
        self.test_path = self.set_test_path()
        self.model_path = self.set_model_path()
        self.param_path = self.set_model_param_path()
        self.hyperparam_path = self.set_model_hyperparam_path()

    def read_config(self) -> dict:
        """
        Read the config yaml file and return the data as a dictionary

        :return: dict, containing the configuration data
        """
        try:
            # change the directory to the configuration folder
            os.chdir(os.path.join("C:/GitProjects/AudioMNIST", "config"))
            # os.chdir(os.path.join(os.getcwd(), "config"))

            # open the configuration folder
            with open(self.cfg_file, "r") as file:
                # load the configuration file into a dictionary
                cfg_setup = yaml.safe_load(file)
        except:
            # raise an error if the filename is not valid
            raise FileNotFoundError(f"{self.cfg_file} is not a valid config filepath!")

        # return the configuration data
        return cfg_setup

    def set_audio_path(self) -> str:
        """
        Get the path to the folder containing each participant's audio data

        :return: str, path to the audio folder
        """
        # Combine the project path and the audio folder path
        return os.path.join(self.cfg_setup["project_path"], "audio")

    def set_meta_data_path(self) -> str:
        """
        Get the path to the file containing meta data information

        :return: str, path to the meta data file
        """
        # Combine the project path and the audio folder path to get the meta data file path
        return os.path.join(
            self.cfg_setup["project_path"], "audio", "audioMNIST_meta.txt"
        )

    def set_data_path(self) -> str:
        """
        Get the path to the folder containing each participant's processed data

        :return: str, path to the processed data folder
        """
        # Combine the project path and the data folder path
        return os.path.join(self.cfg_setup["project_path"], "data")

    def set_plot_path(self) -> str:
        """
        Get the path to the folder containing plots

        :return: str, path to the plot folder
        """
        # Combine the project path and the plots folder path
        return os.path.join(self.cfg_setup["project_path"], "plots")

    def set_result_path(self) -> str:
        """
        Get the path to the folder containing results

        :return: str, path to the plot folder
        """
        # Combine the project path and the results folder path
        return os.path.join(self.cfg_setup["project_path"], "results")

    def set_test_path(self) -> str:
        """
        Get the path to the folder containing tests

        :return: str, path to the test folder
        """
        # Combine the project path and the test folder path
        return os.path.join(self.cfg_setup["project_path"], "test")

    def set_model_path(self) -> str:
        """
        Get the path to the folder containing model parameters

        :return: str, path to the model parameters parameters folder
        """
        # Combine the project path and the parameters folder path
        return os.path.join(self.cfg_setup["project_path"], "parameters")

    def set_model_param_path(self) -> str:
        """
        Get the path to the file containing model parameters information

        :return: str, path to the model parameters file
        """
        # Combine the project path and the parameters folder path to get the model parameters file path
        return os.path.join(self.model_path, "model_parameters.yaml")

    def set_model_hyperparam_path(self) -> str:
        """
        Get the path to the file containing model hyperparameters information

        :return: str, path to the model hyperparameters file
        """
        # Combine the project path and the parameters folder path to get the model hyperparameters file path
        return os.path.join(self.model_path, "model_hyperparameters.yaml")
