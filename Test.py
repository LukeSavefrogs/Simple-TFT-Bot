import pyautogui
import time
import sys

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

    if pyautogui.locateOnScreen("models/Pulsante_GruppoOn.png", confidence=0.9) or pyautogui.locateOnScreen("models/Pulsante_GruppoOff.png", confidence=0.9):
        print("Sei in un gruppo. Esci e rilancia")
        
        LeagueOfLegends.click(pyautogui.locateCenterOnScreen("models/Pulsante_GruppoUscita.png", confidence=0.8))
        # return False
        time.sleep(2)


    if not pyautogui.locateOnScreen("models/Pulsante_InGame_Players.png", confidence=0.7):
        print("Non sei in game")

        print("\nCerco pulsante 'Gioca'")
        gioca = pyautogui.locateOnScreen("models/Pulsante_Gioca.png", confidence=0.8)
        if gioca:
            print("Trovato. Lo clicco")
            pyautogui.click(pyautogui.center(gioca), duration=1, tween=pyautogui.easeOutQuad)
            time.sleep(2)


        print("\nCerco pulsante 'TFT'")
        tft = pyautogui.locateCenterOnScreen("models/Pulsante_TFT.png", confidence=0.8)
        if tft:
            print("Trovato. Lo clicco")
            pyautogui.click(tft, duration=1, tween=pyautogui.easeOutQuad)
            time.sleep(2)
        

        print("\nCerco pulsante 'Conferma'")
        conferma = pyautogui.locateCenterOnScreen("models/Pulsante_Conferma.png", confidence=0.8)
        if conferma: 
            print("Trovato. Lo clicco")

            pyautogui.click(conferma, duration=1, tween=pyautogui.easeOutQuad)
            time.sleep(2)


        print("\nControllo che sia una normal:")
        if not pyautogui.locateCenterOnScreen("models/Scritta_TFT_Normal.png", confidence=0.6):
            print("Non ti trovi in una Normal!!")

            return False



        while pyautogui.locateCenterOnScreen("models/Pulsante_GruppoUscita.png", confidence=0.8):
            print("\nCerco pulsante 'Trova Partita'")
            trova_partita = pyautogui.locateCenterOnScreen("models/Pulsante_TrovaPartita.png", confidence=0.6)
            if trova_partita:
                print("Trovato. Lo clicco")
                pyautogui.click(trova_partita, duration=1, tween=pyautogui.easeOutQuad)



            # Aspetta fino a che non trova una partita
            print()
            while not pyautogui.locateCenterOnScreen("models/Pulsante_AccettaON.png", confidence=0.8):
                print("Ricerca partita in corso...")
                time.sleep(0.5)


            print("Partita Trovata!")

            pulsante_accetta = pyautogui.locateCenterOnScreen("models/Pulsante_AccettaON.png", confidence=0.8)
            pyautogui.click(pulsante_accetta, duration=1, tween=pyautogui.easeOutQuad)
            print("Partita Accettata!")

            time.sleep(0.5)


            # Controllo che non sia stata rifiutata
            # Aspetta fino a che non trova una partita
            print()
            while pyautogui.locateCenterOnScreen("models/Pulsante_AccettaOFF.png", confidence=0.8):
                print("Aspetto che tutti gli altri giocatori accettino...")
                time.sleep(0.5)

            if not pyautogui.locateCenterOnScreen("models/Pulsante_GruppoUscita.png", confidence=0.8):
                print("Aperta schermata di caricamento")
                break

            print("Un giocatore non ha accettato. Sei stato rimesso in coda")

        print()
        # Controllo finchè non entro in partita
        # while not pyautogui.locateOnScreen("models/Pulsante_InGame_LockShop.png", confidence=0.9):
        while not pyautogui.locateOnScreen("models/Pulsante_InGame_Players.png", confidence=0.9):
            print("Caricamento partita in corso...")
            time.sleep(1)


    # Ogni 2 minuti cerco di arrendermi
    if surrend:
        while True:
            pulsante_impostazioni = pyautogui.locateCenterOnScreen("models/Pulsante_InGame_Impostazioni.png", confidence=0.7)
            if not pulsante_impostazioni:
                print("Non trovo pulsante impostazioni")
                continue

            LeagueOfLegends.click(pulsante_impostazioni)

            # Se non riesce ad aprire le Impostazioni va in Timeout e continua
            try: 
                time_before_settings = int(time.time())
                while not pyautogui.locateCenterOnScreen("models/Pulsante_InGame_Annulla.png", confidence=0.7): 
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
            can_surrend = pyautogui.locateCenterOnScreen("models/Pulsante_InGame_ResaOn.png", confidence=0.9)
            print("ON: ", pyautogui.locateCenterOnScreen("models/Pulsante_InGame_ResaOn.png", confidence=0.9))
            print("OFF: ", pyautogui.locateCenterOnScreen("models/Pulsante_InGame_ResaOff.png", confidence=0.9))


            if can_surrend: 
                LeagueOfLegends.click(can_surrend)
                pyautogui.screenshot('Surrend_Round.png')

                while not pyautogui.locateCenterOnScreen("models/Dialog_IngameSurrend.png", confidence=0.9): 
                    print("In attesa del menu di arresa")
                    time.sleep(0.1)


                print("Mi arrendo!")
                LeagueOfLegends.click(pyautogui.locateCenterOnScreen("models/Pulsante_InGame_Resa_Conferma.png", confidence=0.9))
                print("Arreso!")

                break

            # Se non posso arrendermi clicco su Annulla
            pulsante_annulla = pyautogui.locateCenterOnScreen("models/Pulsante_InGame_Annulla.png", confidence=0.9)
            LeagueOfLegends.click(pulsante_annulla)

            print("Aspetto 60 secondi...")
            time.sleep(60)
        
    else:
        while pyautogui.locateCenterOnScreen("models/Pulsante_InGame_Impostazioni.png", confidence=0.7):
            print("Carosello    : ", pyautogui.locateOnScreen("models/InGame_TurnoCaroselloCampioni.png", confidence=0.9))
            print("PVE (Minions): ", pyautogui.locateOnScreen("models/InGame_TurnoPVE-Minions.png", confidence=0.9))
            print("PVE (Krugs)  : ", pyautogui.locateOnScreen("models/InGame_TurnoPVE-Krugs.png", confidence=0.9))
            print("PVE (Lupi)   : ", pyautogui.locateOnScreen("models/InGame_TurnoPVE-Lupi.png", confidence=0.9))
            print("PVP          : ", pyautogui.locateOnScreen("models/InGame_TurnoPVP.png", confidence=0.9))
            print()

            time.sleep(30)
        
    time.sleep(10)
    
    # Clicco su OK quando ricevo missioni (se le trovo)
    while pyautogui.locateCenterOnScreen("models/FinePartita_MissioneCompletata.png", confidence=0.8):
        print("Hai appena portato a termine una missione!")
        mission_finished = pyautogui.locateCenterOnScreen("models/FinePartita_MissioneCompletata.png", confidence=0.8)
        LeagueOfLegends.click(mission_finished)
        time.sleep(2)

    # Aspetto che esca fuori il pulsante "Gioca Ancora"
    while not pyautogui.locateCenterOnScreen("models/Pulsante_GiocaAncora.png", confidence=0.9): 
        print("In attesa del riepilogo con le statistiche di fine partita")
        time.sleep(0.1)

    print("Clicco su 'Gioca Ancora'")
    LeagueOfLegends.click(pyautogui.locateCenterOnScreen("models/Pulsante_GiocaAncora.png", confidence=0.9))
    
    return True


if __name__ == "__main__":
    leagueWindow = pyautogui.getWindowsWithTitle("League of Legends")
    singleGame = False

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

    # print(len(list(pyautogui.locateAllOnScreen("models/TFT_CapsuleGrigie.png", confidence=0.7))))
    # for capsula in pyautogui.locateAllOnScreen("models/TFT_CapsuleBlu.png", confidence=0.7):
    #     print(capsula)
    #     coords = pyautogui.center(capsula)

    #     # pyautogui.moveTo(coords, duration=1.0, tween=pyautogui.easeOutQuad)
    #     # time.sleep(0.5)

    # pyautogui.click()
    

    if singleGame:
        while True: playGame(surrend=True)
    else:
        playGame()