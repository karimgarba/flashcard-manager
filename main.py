# test users based on revision category
#main func
#common sub
#specific sub
import sqlite3

class FlashCard:
    def __init__(self, frontCard, backCard, revCat):
        self.frontCard = frontCard
        self.backCard = backCard
        self.revCat = revCat

def init():
    initDatabase()
    flashcards = loadFlashcards()
    return flashcards

def initDatabase():
    connection = sqlite3.connect('flashcards.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY,
            frontCard TEXT,
            backCard TEXT,
            revCat INTEGER
        )
    ''')
    connection.close()
    
def loadFlashcards():
    flashCards = []

    connection = sqlite3.connect('flashcards.db')
    cursor = connection.cursor()
    cursor.execute('SELECT frontCard, backCard, revCat FROM flashcards')

    rows = cursor.fetchall()
    if rows:
        for row in rows:
            frontCard, backCard, revCat = row
            card = initCard(frontCard, backCard, revCat)
            flashCards.append(card)

    connection.close()

    return flashCards   

def initCard(frontCard, backCard, revCat):
    card = FlashCard(frontCard, backCard, revCat)
    return card

def userAddCards(flashcards):
    while(True):
        frontCard = input("Front: ")
        backCard = input ("Back: ")
        revCat = 0
        newCard = initCard(frontCard, backCard, revCat)
        flashcards.append(newCard)
        while(True):
            choice = int(input("Would you like to add more cards? 1 Yes | 2 No: "))
            if (choice == 1):
                break
            elif (choice == 2):
                return
            else:
                print("Enter a valid option")

def printFlashcards(flashcards):
    count = 1
    for card in flashcards:
        print(f"Flashcard Number: {count}")
        print(f"Front: {card.frontCard}")
        print(f"Back: {card.backCard}")
        print(f"========================================================")
        count+=1

def viewFlashcards(flashcards):
    while(True):
        printFlashcards(flashcards)
        viewMore = input("Press 'q' to exit viewing: ").lower()
        if (viewMore == 'q'):
            return


def writeToDatabase(flashcards):
    connection = sqlite3.connect('flashcards.db')
    cursor = connection.cursor()

    existing_flashcards = loadFlashcards()

    new_flashcards = [card for card in flashcards if card not in existing_flashcards]

    for card in new_flashcards:
        cursor.execute('INSERT INTO flashcards (frontCard, backCard, revCat) VALUES (?, ?, ?)',(card.frontCard, card.backCard, card.revCat))

    connection.commit()
    connection.close()


def deleteFlashcards(flashcards):
    while(True):
        printFlashcards(flashcards)
        choice = (input("What flashcard would you like to delete"))
        while(True):
            if (choice > 0 & choice < len(flashcards)):
                flashcards.pop(choice)
                break
            else:
                print("Enter a valid choice")
            while(True):
                deleteMore = input(("Would you like to delete more cards? 1 Yes | 2 No: "))
                if (deleteMore == 1):
                    break
                elif (deleteMore == 2):
                    return
                else:
                    print("Enter a valid option")

#def reviseCards(flashcards):

    
                
def menu(flashcards):
    while(True):
        menuChoice = int(input("What do you want to do. 1 Add Flashcards | 2 View Flashcards | 3 Delete Flashcards  | 4 Revise Flashcards | 5 Exit: "))
        if (menuChoice == 1):
            print("Add Flashcards")
            print("==============")
            userAddCards(flashcards)
            writeToDatabase(flashcards)
        elif (menuChoice == 2):
            print("View Flashcards")
            print("===============")
            viewFlashcards(flashcards)
        elif (menuChoice == 3):
            print("Delete Flashcards")
            print("=================")
            deleteFlashcards(flashcards)
            writeToDatabase(flashcards)
        elif (menuChoice == 4):
            print("Revise Flashcards")
            print("=================")
            writeToDatabase(flashcards)
        elif (menuChoice == 5):
            print("Exiting...")
            return

def main():
    flashcards = init()
    menu(flashcards)
    return

if (__name__ == '__main__'):
    main()