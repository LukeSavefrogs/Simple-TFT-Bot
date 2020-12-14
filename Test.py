import pyautogui
import time
import sys

def test():  
    print("\nControllo se sei dentro un gruppo: ")

    if pyautogui.locateOnScreen("models/Pulsante_GruppoOn.png", confidence=0.9) or pyautogui.locateOnScreen("models/Pulsante_GruppoOff.png", confidence=0.9):
        print("Sei in un gruppo. Esci e rilancia")
        
        LeagueOfLegends.click(pyautogui.locateCenterOnScreen("models/Pulsante_GruppoUscita.png", confidence=0.8))
        # return False
        time.sleep(2)


    if not pyautogui.locateOnScreen("models/Pulsante_InGame_LockShop.png", confidence=0.9):
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




        print("\nCerco pulsante 'Trova Partita'")
        trova_partita = pyautogui.locateCenterOnScreen("models/Pulsante_TrovaPartita.png", confidence=0.6)
        if trova_partita:
            print("Trovato. Lo clicco")
            pyautogui.click(trova_partita, duration=1, tween=pyautogui.easeOutQuad)



        # Aspetta fino a che non trova una partita
        print()
        while not pyautogui.locateCenterOnScreen("models/Pulsante_Accetta.png", confidence=0.8):
            print("Ricerca partita in corso...")
            time.sleep(0.5)


        print("Partita Trovata!")

        pulsante_accetta = pyautogui.locateCenterOnScreen("models/Pulsante_Accetta.png", confidence=0.9)
        pyautogui.click(pulsante_accetta, duration=1, tween=pyautogui.easeOutQuad)


    # input("Press when started...")

    print()
    # Controllo finchè non entro in partita
    while not pyautogui.locateOnScreen("models/Pulsante_InGame_LockShop.png", confidence=0.9):
        print("Caricamento partita in corso...")
        time.sleep(1)


    # Ogni 2 minuti cerco di arrendermi
    while True:
        # LeagueOfLegends.click()
        # pyautogui.press("esc")
        # pyautogui.keyDown("esc")
        # time.sleep(0.2)
        # pyautogui.keyUp("esc")

        pulsante_impostazioni = pyautogui.locateCenterOnScreen("models/Pulsante_InGame_Impostazioni.png", confidence=0.9)
        LeagueOfLegends.click(pulsante_impostazioni)

        while not pyautogui.locateCenterOnScreen("models/Pulsante_InGame_Annulla.png", confidence=0.9): 
            print("In attesa di Annulla")
            time.sleep(0.1)

        can_surrend = pyautogui.locateCenterOnScreen("models/Pulsante_InGame_ResaOn.png", confidence=0.9)
        print("ON: ", pyautogui.locateCenterOnScreen("models/Pulsante_InGame_ResaOn.png", confidence=0.9))
        print("OFF: ", pyautogui.locateCenterOnScreen("models/Pulsante_InGame_ResaOff.png", confidence=0.9))


        if can_surrend: 
            LeagueOfLegends.click(can_surrend)

            while not pyautogui.locateCenterOnScreen("models/Dialog_IngameSurrend.png", confidence=0.9): 
                print("In attesa del menu di arresa")
                time.sleep(0.1)

            print("Mi arrendo!")
            LeagueOfLegends.click(pyautogui.locateCenterOnScreen("models/Pulsante_InGame_Resa_Conferma.png", confidence=0.9))

            break

        # Se non posso arrendermi clicco su Annulla
        pulsante_annulla = pyautogui.locateCenterOnScreen("models/Pulsante_InGame_Annulla.png", confidence=0.9)
        LeagueOfLegends.click(pulsante_annulla)

        print("Aspetto 60 secondi...")
        time.sleep(60)
    

    # Clicco su OK quando ricevo missioni
    while pyautogui.locateCenterOnScreen("models/FinePartita_MissioneCompletata.png", confidence=0.9):
        print("Hai appena portato a termine una missione!")
        mission_finished = pyautogui.locateCenterOnScreen("models/FinePartita_MissioneCompletata.png", confidence=0.9)
        LeagueOfLegends.click(mission_finished)
        time.sleep(2)

    # Aspetto che esca fuori il pulsante "Gioca Ancora"
    while not pyautogui.locateCenterOnScreen("models/Pulsante_GiocaAncora.png", confidence=0.9): 
        print("In attesa del riepilogo con le statistiche di fine partita")
        time.sleep(0.1)

    LeagueOfLegends.click(pyautogui.locateCenterOnScreen("models/Pulsante_GiocaAncora.png", confidence=0.9))
    return 



class LeagueOfLegends(object):
    @staticmethod
    def click(coordinates=None, button="left"):
        """ Forces a click inside the client
        """
        pyautogui.moveTo(coordinates, duration=1.0, tween=pyautogui.easeOutQuad)
        pyautogui.sleep(0.5)
        pyautogui.mouseDown(button=button); 
        pyautogui.sleep(0.2)
        pyautogui.mouseUp(button=button)


if __name__ == "__main__":
    leagueWindow = pyautogui.getWindowsWithTitle("League of Legends")
    # leagueWindow = pyautogui.getWindowsWithTitle("League of Legends (TM) Client")
    originalWindow = None
   
    if not leagueWindow:
        print("Errore - LoL non aperto")
        sys.exit(1)

    if not leagueWindow[0].isActive:
        print("Porto LoL in primo piano..")
        originalWindow = pyautogui.getActiveWindow()

        leagueWindow[0].activate()
        time.sleep(2)

    test()

    # if originalWindow:
    #     originalWindow.activate()