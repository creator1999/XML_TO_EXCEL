import random
import string


class uid:


    # Set of unique IDs generated within the session



    def generate_unique_id(self):

        unique_ids = set()
        while True:
            # Create a 7-character unique ID using letters and digits
            unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=7))

            # Check if the ID is already in the set, if not, add it and return
            if unique_id not in unique_ids:
                unique_ids.add(unique_id)
                return unique_id



