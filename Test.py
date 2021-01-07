import pyautogui
import time
import sys
import os
import inspect

"""
Compilazione:
pyinstaller --clean --log-level WARN --onefile --uac-admin --add-data "models;models" --name "TFT Bot" .\Test.py
"""

class CodeTimeout(Exception):
    pass


class LeagueOfLegends(object):
    @staticmethod
    def click(coordinates=None, button="left"):
        """ Forces a click inside the client
        """
        pyautogui.moveTo(coordinates, duration=1.0, tween=pyautogui.easeOutQuad)
        pyautogui.sleep(0.5)
        pyautogui.mouseDown(button=button)
        pyautogui.sleep(0.2)
        pyautogui.mouseUp(button=button)


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
    print("\nControllo se sei dentro un gruppo: ")

    if pyautogui.locateOnScreen(getCorrectPath("models/Pulsante_GruppoOn.png"), confidence=0.9) or pyautogui.locateOnScreen(getCorrectPath("models/Pulsante_GruppoOff.png"), confidence=0.9):
        print("Sei in un gruppo. Esci e rilancia")
        
        LeagueOfLegends.click(pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_GruppoUscita.png"), confidence=0.8))
        # return False
        time.sleep(2)


    if not pyautogui.locateOnScreen(getCorrectPath("models/Pulsante_InGame_Players.png"), confidence=0.7):
        print("Non sei in game")

        print("\nCerco pulsante 'Gioca'")
        gioca = pyautogui.locateOnScreen(getCorrectPath("models/Pulsante_Gioca.png"), confidence=0.8)
        if gioca:
            print("Trovato. Lo clicco")
            pyautogui.click(pyautogui.center(gioca), duration=1, tween=pyautogui.easeOutQuad)
            time.sleep(2)


        print("\nCerco pulsante 'TFT'")
        tft = pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_TFT.png"), confidence=0.8)
        if tft:
            print("Trovato. Lo clicco")
            pyautogui.click(tft, duration=1, tween=pyautogui.easeOutQuad)
            time.sleep(2)
        

        print("\nCerco pulsante 'Conferma'")
        conferma = pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_Conferma.png"), confidence=0.8)
        if conferma: 
            print("Trovato. Lo clicco")

            pyautogui.click(conferma, duration=1, tween=pyautogui.easeOutQuad)
            time.sleep(2)


        print("\nControllo che sia una normal:")
        if not pyautogui.locateCenterOnScreen(getCorrectPath("models/Scritta_TFT_Normal.png"), confidence=0.6):
            print("Non ti trovi in una Normal!!")

            return False



        while pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_GruppoUscita.png"), confidence=0.8):
            print("\nCerco pulsante 'Trova Partita'")
            trova_partita = pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_TrovaPartita.png"), confidence=0.6)
            if trova_partita:
                print("Trovato. Lo clicco")
                pyautogui.click(trova_partita, duration=1, tween=pyautogui.easeOutQuad)



            # Aspetta fino a che non trova una partita
            print()
            while not pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_AccettaON.png"), confidence=0.8):
                print("Ricerca partita in corso...")
                time.sleep(0.5)


            print("Partita Trovata!")

            pulsante_accetta = pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_AccettaON.png"), confidence=0.8)
            pyautogui.click(pulsante_accetta, duration=1, tween=pyautogui.easeOutQuad)
            print("Partita Accettata!")

            time.sleep(0.5)


            # Controllo che non sia stata rifiutata
            # Aspetta fino a che non trova una partita
            print()
            while pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_AccettaOFF.png"), confidence=0.8):
                print("Aspetto che tutti gli altri giocatori accettino...")
                time.sleep(0.5)

            if not pyautogui.locateCenterOnScreen(getCorrectPath("models/Pulsante_GruppoUscita.png"), confidence=0.8):
                print("Aperta schermata di caricamento")
                break

            print("Un giocatore non ha accettato. Sei stato rimesso in coda")

        print()
        # Controllo finchè non entro in partita
        # while not pyautogui.locateOnScreen(getCorrectPath("models/Pulsante_InGame_LockShop.png"), confidence=0.9):
        while not pyautogui.locateOnScreen(getCorrectPath("models/Pulsante_InGame_Players.png"), confidence=0.9):
            print("Caricamento partita in corso...")
            time.sleep(1)


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
    
    return True


if __name__ == "__main__":
    PLAY_SINGLE_GAME = False
    SURREND_WHEN_POSSIBLE = True
    
    leagueWindow = pyautogui.getWindowsWithTitle("League of Legends")

    # Se LoL non è aperto, esce
    if not leagueWindow:
        print("Errore - LoL non aperto")
        sys.exit(1)

    # Porta 'League of Legends' in primo piano (anche se minimizzato) 
    if not leagueWindow[0].isActive:
        print("Porto LoL in primo piano..")
        leagueWindow[0].activate()
        time.sleep(2)

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