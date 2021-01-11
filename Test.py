import pyautogui
import time
import sys
import os
import inspect
import datetime

from pygetwindow import PyGetWindowException

"""
Compilazione:
pyinstaller --clean --log-level WARN --onefile --uac-admin --add-data "models;models" --name "TFT Bot" .\Test.py
"""

class CodeTimeout(Exception):
    pass


class LeagueOfLegends(object):
    @staticmethod
    def click(coordinates=None, button="left", checkIfActive=True):
        """ Forces a click inside the client
        """
        if checkIfActive: LeagueOfLegends.forceActive()

        pyautogui.moveTo(coordinates, duration=1.0, tween=pyautogui.easeOutQuad)
        pyautogui.sleep(0.5)
        pyautogui.mouseDown(button=button)
        pyautogui.sleep(0.2)
        pyautogui.mouseUp(button=button)

    @staticmethod
    def forceActive():
        leagueWindow = pyautogui.getWindowsWithTitle("League of Legends")
        print(leagueWindow)
        
        # Se LoL non è aperto, esce
        if not leagueWindow:
            print("Errore - LoL non aperto")
            return False

        # Porta 'League of Legends' in primo piano (anche se minimizzato) 
        if not leagueWindow[0].isActive:
            print("Porto LoL in primo piano..")
            try:
                leagueWindow[0].activate()
            except PyGetWindowException as e:
                print("WARNING - pygetwindow.PyGetWindowException: " + str(e))

            time.sleep(2)

    @staticmethod
    def isInGame():
        leagueWindow = pyautogui.getWindowsWithTitle("League of Legends")
        print(leagueWindow)
        
        # Se LoL non è aperto, esce
        return len(leagueWindow) > 1


def getCorrectPath(filePath):
	"""Returns the correct path (relative/absolute) wether is a frozen app or a script 
	Args:
		filePath (str): The path to the resource you need
	Returns:
		str: Final resolved path
	"""
	# Se il percorso specificato è assoluto non fare nulla
	if os.path.isabs(filePath):
		return filePath


	# Se è un'applicazione PyInstaller e il percorso è relativo
	if hasattr(sys, "_MEIPASS"):
		file = os.path.join(sys._MEIPASS, filePath)
	
	# Se è uno script e il percorso è relativo
	else:
		# Scopro il percorso del file chiamante
		frame = inspect.stack()[1]
		caller_filename = frame[0].f_code.co_filename

		# Prendo la cartella parent del file chiamante
		caller_working_directory = os.path.dirname(os.path.realpath(caller_filename))

		# Risolvo i percorsi relativi alla cartella in cui è presente lo script chiamante
		file = os.path.abspath(os.path.join(caller_working_directory, filePath))


		# print(f"Caller: {caller_filename}")
		# print(f"Caller WD: {caller_working_directory}")
		# print(f"Final path: {file}\n")

	return file


def playGame(surrend=True):
    """Plays a game

    Args:
        surrend (bool, optional): Whether to surrend as soon as possible. Defaults to True.

    Raises:
        CodeTimeout: [description]

    Returns:
        bool: If succeed
    """
    if not LeagueOfLegends.isInGame():
        print("INFO - Non sei in game (sei ancora nel Client)")

        if pyautogui.locateOnScreen(getCorrectPath("models/Pulsante_GruppoOn.png"), confidence=0.9) or pyautogui.locateOnScreen(getCorrectPath("models/Pulsante_GruppoOff.png"), confidence=0.9):
            print("INFO - Sei gia' in un gruppo")
            
            not_in_lobby = pyautogui.locateOnScreen(getCorrectPath("models/Pulsante_GruppoOn.png"), confidence=0.9)
            if not_in_lobby:
                print("INFO - Non sei nella lobby. Ci entro")
                LeagueOfLegends.click(not_in_lobby)
                time.sleep(2)

                pyautogui.locateOnScreen(getCorrectPath("models/Pulsante_GruppoOff.png"), confidence=0.9)
                try: 
                    time_before_lobby = int(time.time())
                    while not pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_GruppoOff.png"), confidence=0.7): 
                        sec_timeout = int(time.time()) - time_before_lobby
                        print(f"\tIn attesa di Lobby (Elapsed: {sec_timeout}s)")

                        if sec_timeout > 20: 
                            print ("Timeout: In attesa di Lobby")
                            raise CodeTimeout()
                        
                        time.sleep(0.1)
                except CodeTimeout:
                    print ("Timeout - Non sono tornato nella lobby entro 20 secondi")
                    return False
            # pulsante_esci_gruppo = pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_GruppoUscita.png"), confidence=0.8)
            # LeagueOfLegends.click(pulsante_esci_gruppo)

        
        if not pyautogui.locateOnScreen(getCorrectPath("models/Pulsante_Gioca.png"), confidence=0.8) and not pyautogui.locateCenterOnScreen(getCorrectPath("models/Scritta_TFT_Normal.png"), confidence=0.6): 
            print("ERRORE - Non ti trovi in una lobby per una TFT Normal!!")
            LeagueOfLegends.click(pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_GruppoUscita.png"), confidence=0.8))
            
            try: 
                time_before_lobby = int(time.time())
                while not pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_Gioca.png"), confidence=0.7): 
                    sec_timeout = int(time.time()) - time_before_lobby
                    print(f"\tIn attesa di Pulsante 'Gioca' (Elapsed: {sec_timeout}s)")

                    if sec_timeout > 20: 
                        print ("Timeout: In attesa di Pulsante 'Gioca'")
                        raise CodeTimeout()
                    
                    time.sleep(0.1)
            except CodeTimeout:
                print ("Timeout - Non sono tornato nella home entro 20 secondi")
                return False


        gioca = pyautogui.locateOnScreen(getCorrectPath("models/Pulsante_Gioca.png"), confidence=0.8)
        if gioca:
            print("INFO - Non sei in un gruppo. Clicco su pulsante 'Gioca'")
            pyautogui.click(pyautogui.center(gioca), duration=1, tween=pyautogui.easeOutQuad)
            time.sleep(2)

            print("Cerco modalita' 'Teamfight Tactics': \t", end="", flush=True)
            tft = pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_TFT.png"), confidence=0.7)
            if tft:
                print("OK - Lo clicco")
                pyautogui.click(tft, duration=1, tween=pyautogui.easeOutQuad)
                time.sleep(2)
            else: 
                print("ERRORE - Non trovata. Esco")

                pulsante_home = pyautogui.locateCenterOnScreen(getCorrectPath("models/Client_Home.png"), confidence=0.8)
                if not pulsante_home:
                    print ("\n\nERRORE - NON TROVO PULSANTE HOME\n\n")
                    return False

                LeagueOfLegends.click(pulsante_home)

                return False

            print("\nCerco pulsante 'Conferma'")
            conferma = pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_Conferma.png"), confidence=0.8)
            if conferma: 
                print("Trovato. Lo clicco")

                pyautogui.click(conferma, duration=1, tween=pyautogui.easeOutQuad)
                time.sleep(2)


        print("\nCerco pulsante 'Trova Partita': \t", end="", flush=True)
        trova_partita = pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_TrovaPartita.png"), confidence=0.6)
        if not trova_partita: 
            print("ERRORE - Pulsante non trovato\n")
            time.sleep(5)
            return False
        print("OK - Pulsante trovato\n")

        while pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_GruppoUscita.png"), confidence=0.8):
            print("Clicco pulsante 'Trova Partita': \t", end="", flush=True)
            trova_partita = pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_TrovaPartita.png"), confidence=0.6)
            
            if trova_partita: 
                print("OK - Pulsante trovato\n")
                pyautogui.click(trova_partita, duration=1, tween=pyautogui.easeOutQuad)



            # Aspetta fino a che non trova una partita
            if not pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_AccettaON.png")):
                print("Inizio ricerca partita:")
                temp_time = int(time.time())
                while not pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_AccettaON.png"), confidence=0.8):
                    print(f"\t- Ricerca partita in corso... (Elapsed: {int(time.time()) - temp_time}s)")
                    time.sleep(1)

                print("Partita Trovata!")

            pulsante_accetta = pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_AccettaON.png"), confidence=0.8)
            pyautogui.click(pulsante_accetta, duration=1, tween=pyautogui.easeOutQuad)
            print("Partita Accettata!\n")

            time.sleep(0.5)


            # Controllo che non sia stata rifiutata
            # Aspetta fino a che non trova una partita
            print("Aspetto che tutti gli altri giocatori accettino: \t", end="", flush=True)
            try:
                temp_time = int(time.time())
                while pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_AccettaOFF.png"), confidence=0.8):
                    elapsed = int(time.time()) - temp_time
                    if elapsed > 30: 
                        raise CodeTimeout()
                    
                    time.sleep(0.1)
            except CodeTimeout:
                print ("Timeout - Esco")
                continue
            
            print ("OK")
 
            # try: 
            #     time_before_settings = int(time.time())
            #     while not pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_InGame_Annulla.png"), confidence=0.7): 
            #         print("In attesa di Annulla")
            #         sec_timeout = int(time.time()) - time_before_settings
            #         if sec_timeout > 10: 
            #             print ("Timeout: In attesa di Annulla")
            #             raise CodeTimeout()
                    
            #         time.sleep(0.1)
            # except CodeTimeout:
            #     print ("Timeout - Continuo")

            #     continue
            if not pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_GruppoUscita.png"), confidence=0.8):
                print("Aperta schermata di caricamento")
                break

            print("Un giocatore non ha accettato. Sei stato rimesso in coda")

        print()
    
    # Se ancora non è caricata la partita
    if not pyautogui.locateOnScreen(getCorrectPath("models/Pulsante_InGame_Players.png")):
        print("Partita in fase di caricamento:")

        # Controllo finchè non entro in partita
        # while not pyautogui.locateOnScreen(getCorrectPath("models/Pulsante_InGame_LockShop.png"), confidence=0.9):
        temp_time = int(time.time())
        while not pyautogui.locateOnScreen(getCorrectPath("models/Pulsante_InGame_Players.png"), confidence=0.9):
            print(f"\t- Caricamento partita in corso... (Elapsed: {int(time.time()) - temp_time}s)")
            time.sleep(5)

    print()
    game_start = int(time.time())
    
    # Ogni 2 minuti cerco di arrendermi
    if surrend:
        time_settings = None
        while True:
            if not time_settings: time_settings = int(time.time())
            try: 
                pulsante_impostazioni = pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_InGame_Impostazioni.png"), confidence=0.7)
                sec_timeout = int(time.time()) - time_settings

                if sec_timeout > 10: 
                    break

                if not pulsante_impostazioni:
                    print(f"Non trovo pulsante impostazioni ({sec_timeout})")
                    continue
            except CodeTimeout:
                print ("Timeout - Esco")

                continue
            
            time_settings = None

            LeagueOfLegends.click(pulsante_impostazioni)

            # Se non riesce ad aprire le Impostazioni va in Timeout e continua
            try: 
                time_before_settings = int(time.time())
                while not pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_InGame_Annulla.png"), confidence=0.7): 
                    print("In attesa di Annulla")
                    sec_timeout = int(time.time()) - time_before_settings
                    if sec_timeout > 10: 
                        print ("Timeout: In attesa di Annulla")
                        raise CodeTimeout()
                    
                    time.sleep(0.1)
            except CodeTimeout:
                print ("Timeout - Continuo")

                continue

            
            # Controlla se è possibile arrendersi
            can_surrend = pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_InGame_ResaOn.png"), confidence=0.9)
            print("ON: ", pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_InGame_ResaOn.png"), confidence=0.9))
            print("OFF: ", pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_InGame_ResaOff.png"), confidence=0.9))


            if can_surrend: 
                LeagueOfLegends.click(can_surrend)
                # pyautogui.screenshot('Surrend_Round.png')

                try: 
                    time_before = int(time.time())
                    while not pyautogui.locateCenterOnScreen(getCorrectPath("models/Dialog_IngameSurrend.png"), confidence=0.8): 
                        sec_timeout = int(time.time()) - time_before
                        if sec_timeout > 10: 
                            print ("Timeout: In attesa del menu di arresa")
                            raise CodeTimeout()
                        
                        print("In attesa del menu di arresa")
                        time.sleep(0.5)
                except CodeTimeout:
                    print ("Timeout - Continuo")

                    continue


                print("Mi arrendo!")
                LeagueOfLegends.click(pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_InGame_Resa_Conferma.png"), confidence=0.9))
                print("Arreso!")

                break

            # Se non posso arrendermi clicco su Annulla
            pulsante_annulla = pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_InGame_Annulla.png"), confidence=0.9)
            LeagueOfLegends.click(pulsante_annulla)

            print("Aspetto 60 secondi...")
            time.sleep(60)
        
    else:
        while pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_InGame_Impostazioni.png"), confidence=0.7):
            print("Carosello    : ", pyautogui.locateOnScreen(getCorrectPath("models/InGame_TurnoCaroselloCampioni.png"), confidence=0.9))
            print("PVE (Minions): ", pyautogui.locateOnScreen(getCorrectPath("models/InGame_TurnoPVE-Minions.png"), confidence=0.9))
            print("PVE (Krugs)  : ", pyautogui.locateOnScreen(getCorrectPath("models/InGame_TurnoPVE-Krugs.png"), confidence=0.9))
            print("PVE (Lupi)   : ", pyautogui.locateOnScreen(getCorrectPath("models/InGame_TurnoPVE-Lupi.png"), confidence=0.9))
            print("PVP          : ", pyautogui.locateOnScreen(getCorrectPath("models/InGame_TurnoPVP.png"), confidence=0.9))
            print()

            time.sleep(30)
    
    game_end = int(time.time())
    game_duration = datetime.timedelta(seconds=(game_end - game_start))
    print(f"Total Game duration: {game_duration}")
    time.sleep(10)
    
    # Clicco su OK quando ricevo missioni (se le trovo)
    while pyautogui.locateCenterOnScreen(getCorrectPath("models/FinePartita_MissioneCompletata.png"), confidence=0.8):
        print("Hai appena portato a termine una missione!")
        mission_finished = pyautogui.locateCenterOnScreen(getCorrectPath("models/FinePartita_MissioneCompletata.png"), confidence=0.8)
        LeagueOfLegends.click(mission_finished)
        time.sleep(2)

    # Aspetto che esca fuori il pulsante "Gioca Ancora"
    while not pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_GiocaAncora.png"), confidence=0.9): 
        print("In attesa del riepilogo con le statistiche di fine partita")
        time.sleep(0.1)

    print("Clicco su 'Gioca Ancora'")
    LeagueOfLegends.click(pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_GiocaAncora.png"), confidence=0.9))
    
    time.sleep(2)
    premi = pyautogui.locateCenterOnScreen(getCorrectPath("models/Client_Prizes.png"), confidence=0.8)
    if premi: 
        LeagueOfLegends.click(premi)

        try: 
            time_before = int(time.time())
            while not pyautogui.locateCenterOnScreen(getCorrectPath("models/Client_Prizes_Add.png"), confidence=0.8): 
                sec_timeout = int(time.time()) - time_before
                if sec_timeout > 10: 
                    print ("Timeout: In attesa del caricamento dei Premi")
                    raise CodeTimeout()
                
                print("In attesa del caricamento dei Premi")
                time.sleep(0.5)
        except CodeTimeout:
            print ("Timeout - Continuo")

        pyautogui.screenshot('StatoMedaglie.png')
            
    return True


if __name__ == "__main__":
    PLAY_SINGLE_GAME = False
    SURREND_WHEN_POSSIBLE = True

    # Porta 'League of Legends' in primo piano (anche se minimizzato) 
    LeagueOfLegends.forceActive()

    # print(pyautogui.KEYBOARD_KEYS)

    # print(len(list(pyautogui.locateAllOnScreen(getCorrectPath("models/TFT_CapsuleGrigie.png"), confidence=0.7))))
    # for capsula in pyautogui.locateAllOnScreen(getCorrectPath("models/TFT_CapsuleBlu.png"), confidence=0.7):
    #     print(capsula)
    #     coords = pyautogui.center(capsula)

    #     # pyautogui.moveTo(coords, duration=1.0, tween=pyautogui.easeOutQuad)
    #     # time.sleep(0.5)

    # pyautogui.click()
    
    while True: 
        playGame(surrend=SURREND_WHEN_POSSIBLE)

        if PLAY_SINGLE_GAME: break