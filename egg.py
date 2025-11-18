import sqlite3, json
class Egg:
    """This class deals with the creation and possible management of files
    worked by the Dragon class. When the Dragon is created, it also creates
    an Egg with the given format, which automatically checks whether the files
    we will be working with exist.
    If these files do not exist, create them. Specially important for the SQL file,
    which will have procedures to take in data."""
    def __init__(self, file:str, resource:str, format:str) -> None:
        self.working_file = file
        self.resource = resource
        self.offset = 0
        if format == 'sql':
            self.crack_sql()
        elif format == 'json':
            self.empty = self.crack_json()

    def crack_json(self) -> bool:
        try:
            with open(self.working_file, mode='r') as file:
                print(f'File "{self.working_file}" found.')
                saved_data = json.load(file)
                self.offset = len(saved_data)
        except FileNotFoundError:
            print(f'File "{self.working_file}" not found. Creating new one...')
            with open(self.working_file, mode='w') as file:
                print(f'File "{self.working_file}" successfuly created.')
            return True # True if file is empty
        else:
            return False # False if file is not empty


    def crack_sql(self):
        """Called at init to check if a db already exists. If not, create it."""
        conn = sqlite3.connect(self.working_file)
        cursor = conn.cursor()
        tbl_generator = f"""
            CREATE TABLE IF NOT EXISTS {self.resource} (
                pid INTEGER PRIMARY KEY AUTOINCREMENT,
                aliases,
                api_detail_url,
                birth,
                count_of_issue_appearances,
                date_added,
                date_last_updated,
                deck,
                description,
                first_appeared_in_issue,
                gender,
                id NOT NULL,
                image,
                name,
                origin,
                publisher,
                real_name,
                site_detail_url);"""
        cursor.execute(tbl_generator)

        # Create a procedure to process incoming data
        parse_json_procedure = f"""

        """
        insert_procedure = f"""
        CREATE PROCEDURE insert_{self.resource}_data
            @aliases = NULL,
            @api_detail_url = NULL,
            @birth = NULL,
            @count_of_issue_appearances = NULL,
            @date_added = NULL,
            @date_last_updated = NULL,
            @deck = NULL,
            @description = NULL,
            @first_appeared_in_issue = NULL,
            @gender = NULL,
            @id,
            @image = NULL,
            @name = NULL,
            @origin = NULL,
            @publisher = NULL,
            @real_name = NULL,
            @site_detail_url = NULL
        AS
        BEGIN
            INSERT INTO {self.resource}
                (
                aliases,
                api_detail_url,
                birth,
                count_of_issue_appearances,
                date_added,
                date_last_updated,
                deck,
                description,
                first_appeared_in_issue,
                gender,
                id NOT NULL,
                image,
                name,
                origin,
                publisher,
                real_name,
                site_detail_url
                )
            VALUES
                (
                @aliases,
                @api_detail_url,
                @birth,
                @ount_of_issue_appearances,
                @date_added,
                @date_last_updated,
                @deck,
                @description,
                @first_appeared_in_issue,
                @gender,
                @id NOT NULL,
                @image,
                @name,
                @origin,
                @publisher,
                @real_name,
                @site_detail_url
                )
        END
        GO"""
        conn.close()

    def get_offset(self) -> int:
        return self.offset