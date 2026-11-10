
import sqlite3

conn = sqlite3.connect("pets.db")
cursor = conn.cursor()

while True:
    person_id = input("Enter a person's ID (-1 to quit): ")

    try:
        person_id = int(person_id)
    except ValueError:
        print("Please enter a valid number.")
        continue

    if person_id == -1:
        print("Goodbye!")
        break

    cursor.execute(
        "SELECT * FROM person WHERE id = ?",
        (person_id,)
    )
    person = cursor.fetchone()

    if person is None:
        print("Person not found.")
        continue

    first_name = person[1]
    last_name = person[2]
    age = person[3]

    print(f"{first_name} {last_name}, {age} years old")

    cursor.execute("""
        SELECT pet.name, pet.breed, pet.age, pet.dead
        FROM pet
        JOIN person_pet ON pet.id = person_pet.pet_id
        WHERE person_pet.person_id = ?
    """, (person_id,))

    pets = cursor.fetchall()

    for pet in pets:
        name, breed, pet_age, dead = pet

        print(
            f"{first_name} {last_name} owned {name}, "
            f"a {breed}, that was {pet_age} years old."
        )

        if dead == 1:
            print(f"{name} is deceased.")
        else:
            print(f"{name} is alive.")

conn.close()
