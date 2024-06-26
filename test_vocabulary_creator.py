from vocabulary_creator import VocabularyCreator
import unittest
from unittest.mock import patch

class TestVocabularyCreator(unittest.TestCase):
    def setUp(self):
        # données pour mocker "return_value" du "load_dict"
        self.mails = {"dataset": [
                        {
                        "mail": {
                        "Subject": " no more outdated software ! upgrade !",
                        "From": "GP@paris.com",
                        "Date": "2005-03-04",
                        "Body":"we get you the best deal ! skip the retail box and save !\namazing special # 1 "
                               ":\nadobe - photoshop 7 premiere 7 illustrator 10 = only $ 120\namazing special # 2 "
                               ":\nwindows xp professional + microsoft office xp professional = only $ 80\namazing "
                               "special # 3 :\nadobe photoshop cs + adobe illustrator cs + adobe indesign cs\namazing "
                               "special # 4 :\nmacromedia dreamwaver mx 2004 + flash mx 2004 = only $ 100\nalso "
                               ":\nwindows xp professional with sp 2 full version\noffice xp professionaloffice 2003 "
                               "professional ( 1 cd edition )\noffice 2000 premium edition ( 2 cd )\noffice 97 sr "
                               "2\noffice xp professional\noffice 2000\noffice 97\nms plus\nms sql server 2000 "
                               "enterprise edition\nms visual studio . net architect edition\nms encarta encyclopedia "
                               "delux 2004\nms project 2003 professional\nms money 2004\nms streets and trips "
                               "2004\nms works 7\nms picture it premium 9\nms exchange 2003 enterprise server\nadobe "
                               "photoshop\nwindows 2003 server\nwindows 2000 workstation\nwindows 2000 "
                               "server\nwindows 2000 advanced server\nwindows 2000 datacenter\nwindows nt 4 . "
                               "0\nwindows millenium\nwindows 98 second edition\nwindows 95\ncorel draw graphics "
                               "suite 12\ncorel draw graphics suite 11\ncorel photo painter 8\ncorel word perfect "
                               "office 2002\nadobe pagemaker\nadobe illustrator\nadobe acrobat 6 professional\nadobe "
                               "premiere\nmacromedia dreamwaver mx 2004\nmacromedia flash mx 2004\nmacromedia "
                               "fireworks mx 2004\nmacromedia freehand mx 11\nnorton system works 2003\nborland "
                               "delphi 7 enterprise edition\nquark xpress 6 passport multilanguage\nyou need to save "
                               "some money somewhere . let it be here !\nstop mailing now .\nask him for advice about "
                               "something important to you . let s have a bbq tomorrow and celebrate me . i guess 8 "
                               "ffm 9 lj 863676 r 5 r 2 vym 314 hk 79 nnu 27 e 64 m 6 bb \n",
                        "Spam": "true",
                        "File": "enronds//enron4/spam/4536.2005-03-04.GP.spam.txt"
                        }

                        },
                        {
                            "mail": {
                                "Subject": " re : louise kitchen s visit to monterrey",
                                "From": "kitchen@paris.com",
                                "Date": "2001-06-28",
                                "Body": "louise i am sending you the agenda for your visit to monterrey .\n- 11 : 00 am - arrival to the airport . miguel angel rodriguez and i will pick you up at the exit of the international arrival area at the monterrey airport .\n- 12 : 00 pm - overall introduction to edem team participants : ( all the office ) .\n- 13 : 00 pm - lunch @ the office . we ll bring some non - spicy but traditional mexican food .\n- 14 : 00 pm - commercial meeting\nproject overview : vitro texmex fapsa baja coal project other .\nparticipants : irvin alatorre sabine duffy perez gonzalez lenci and williams .\n- 16 : 00 pm - commercial meeting\nrisk management overview : current structures marketing strategy for the remainder of the year .\nparticipants : irvin alatorre sabine duffy perez gonzalez lenci and williams .\n- 17 : 45 pm - departure to airport ( plane leaves at 7 : 20 so there should be plenty of time ) .\nbest regards \n",
                                "Spam": "false",
                                "File": "enronds//enron3/ham/1362.2001-06-28.kitchen.ham.txt"
                            }

                        },
                    ]}
        self.clean_subject_spam = ["no", "more"]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_spam = ["best", "deal","deal","deal","important","important","important"]  # données pour mocker "return_value" du "clean_text"
        self.clean_subject_ham = ["louise", "kitchen"]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_ham = ["agenda","agenda", "visit"]  # données pour mocker "return_value" du "clean_text"
        # vocabulaire avec les valeurs de la probabilité calculées correctement
        self.vocab_expected = { 'p_sub_spam': {'no': 1/2, 'more': 1/2},
                                'p_sub_ham': {'louise': 0.5, 'kitchen': 0.5},
                                'p_body_spam': {'best': 1/7, 'deal': 3/7, 'important': 3/7},
                                'p_body_ham': {'agenda': 2/3, 'visit': 1/3}}

    def tearDown(self):
        pass

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    @patch("vocabulary_creator.TextCleaning.clean_text")
    @patch("vocabulary_creator.VocabularyCreator.write_data_to_vocab_file")
    def test_create_vocab_spam_Returns_vocabulary_with_correct_values(
        self, mock_write_data_to_vocab_file, mock_clean_text, mock_load_dict
    ):
        """Description: Tester qu'un vocabulaire avec les probabilités calculées
        correctement va être retourné. Il faut mocker les fonctions "load dict"
         (utiliser self.mails comme une simulation de valeur de retour),"clean text"
         (cette fonction va être appelée quelques fois, pour chaque appel on
         va simuler une valeur de retour differente, pour cela il faut utiliser
         side_effect (voir l'exemple dans l'énonce)) et
         "write_data_to_vocab_file" qui va simuler "return True" au lieu
         d'écrire au fichier "vocabulary.json".
         if faut utiliser self.assertEqual(appel_a_create_vocab(), self.vocab_expected)
        """
        mock_load_dict.return_value = self.mails

        list_of_values = [self.clean_body_ham, self.clean_subject_ham,
                          self.clean_body_spam, self.clean_subject_spam]
        def side_effect(text):
            return list_of_values.pop()
        mock_clean_text.side_effect = side_effect

        vocabularyCreator = VocabularyCreator()
        vocabularyCreator.create_vocab()
        mock_write_data_to_vocab_file.assert_called_once_with(self.vocab_expected)


    ###########################################
    #               CUSTOM TEST               #
    ###########################################