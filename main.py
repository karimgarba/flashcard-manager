# Import the sqlite3 module for database operations
import sqlite3

# Define the FlashCard class to represent flashcards
class FlashCard:
    def __init__(self, id, frontCard, backCard, revCat):
        self.id = id
        self.frontCard = frontCard
        self.backCard = backCard
        self.revCat = revCat

    # Method to update the revision category of the flashcard
    def updateRevCat(self, correct=True):
        if correct:
            # Increase the revision category by 1 if the revision was correct
            self.revCat += 1
        else:
            # Reset the revision category to 0 if the revision was incorrect
            self.revCat = 0

# Initialize the flashcard database and load existing flashcards
def init():
    initDatabase()
    flashcards = loadFlashcards()
    return flashcards

# Initialize the flashcard database by creating a table if it doesn't exist
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

# Load existing flashcards from the database
def loadFlashcards():
    flashCards = []

    connection = sqlite3.connect('flashcards.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, frontCard, backCard, revCat FROM flashcards')

    rows = cursor.fetchall()
    if rows:
        for row in rows:
            id, frontCard, backCard, revCat = row
            card = FlashCard(id, frontCard, backCard, revCat)
            flashCards.append(card)

    connection.close()

    return flashCards   

# Write new flashcards to the database
def writeToDatabase(flashcards):
    connection = sqlite3.connect('flashcards.db')
    cursor = connection.cursor()

    existing_flashcards = loadFlashcards()
    new_flashcards = [card for card in flashcards if card.id is None]

    for card in new_flashcards:
        cursor.execute('INSERT INTO flashcards (frontCard, backCard, revCat) VALUES (?, ?, ?)',(card.frontCard, card.backCard, card.revCat))
        cursor.execute('SELECT last_insert_rowid()')  # Retrieve the last inserted ID
        card.id = cursor.fetchone()[0]  # Update the card object with the new ID

    connection.commit()
    connection.close()

# Function for user to add new flashcards
def userAddCards(flashcards):
    while True:
        frontCard = input("Front: ")
        backCard = input ("Back: ")
        revCat = 0
        newCard = FlashCard(None, frontCard, backCard, revCat)
        flashcards.append(newCard)
        while True:
            choice = int(input("Would you like to add more cards? 1 Yes | 2 No: "))
            if choice == 1:
                break
            elif choice == 2:
                writeToDatabase(flashcards)
                return
            else:
                print("Enter a valid option")

# Function to print all flashcards
def printFlashcards(flashcards):
    count = 1
    for card in flashcards:
        print(f"Flashcard Number: {card.id}")
        print(f"Front: {card.frontCard}")
        print(f"Back: {card.backCard}")
        print(f"Revision Category: {card.revCat}")
        print("========================================================")
        count += 1

# Function to view flashcards
def viewFlashcards(flashcards):
    while True:
        printFlashcards(flashcards)
        viewMore = input("Press '1' to exit viewing: ")
        if viewMore == '1':
            return

# Function to delete flashcards
def deleteFlashcards(flashcards):
    while True:
        printFlashcards(flashcards)
        choice = int(input("Enter the ID of the flashcard you would like to delete: "))
        cardToDelete = next((card for card in flashcards if card.id == choice), None)
        if cardToDelete:
            flashcards.remove(cardToDelete)
            connection = sqlite3.connect('flashcards.db')
            cursor = connection.cursor()
            cursor.execute('DELETE FROM flashcards WHERE id = ?', (choice,))
            connection.commit()
            connection.close()
            print("Flashcard deleted successfully.")
        else:
            print("Enter a valid ID.")

        while True:
            deleteMore = input("Would you like to delete more cards? 1 Yes | 2 No: ")
            if deleteMore == '1':
                break
            elif deleteMore == '2':
                writeToDatabase(flashcards)
                return
            else:
                print("Enter a valid option")

# Function to create study sets based on revision categories
def createStudySet(flashcards):
    studySets = {}  # Dictionary to hold study sets
    for card in flashcards:
        revCat = card.revCat
        if revCat not in studySets:
            studySets[revCat] = [card]  # If the revision category doesn't exist, create a new list with the card
        else:
            studySets[revCat].append(card)  # If the revision category exists, append the card to the existing list
    return studySets

# Function to revise flashcards
def reviseFlashcards(flashcards):
    studySets = createStudySet(flashcards)

    # Sort study sets by revision category in ascending order
    sorted_studySets = sorted(studySets.items(), key=lambda x: x[0])

    for revCat, studySet in sorted_studySets:
        print(f"Study Set for Revision Category {revCat + 1}:")
        print(f"========================================")
        for card in studySet:
            print(f"Front: {card.frontCard}")
            viewBackResponse = input("Press '1' to view the back: ")
            if viewBackResponse == '1':
                print(f"Back: {card.backCard}")
            markResponse = input("Did you revise this card? 1 Yes | 2 No: ")
            if markResponse == '1':
                card.updateRevCat(correct=True)
                print("Well done!")
            else:
                card.updateRevCat(correct=False)
                print("Card marked for further revision.")

    writeToDatabase(flashcards)

# Function for the main menu
def menu(flashcards):
    while True:
        menuChoice = int(input("What do you want to do. 1 Add Flashcards | 2 View Flashcards | 3 Delete Flashcards  | 4 Revise Flashcards | 5 Exit: "))
        if menuChoice == 1:
            print("Add Flashcards")
            print("==============")
            userAddCards(flashcards)