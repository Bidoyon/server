import dump from "mysqldump";
import * as path from "path";
import * as fs from "fs";

export default class Backup {
    /**
     * The backups folder
     */
    static folder: string = path.join(__dirname, "../../../../backups")
    /**
     * The name of the database
     */
    public readonly database: string
    /**
     * The date when the backup was created
     */
    public readonly date: Date
    /**
     * The name of the backup
     */
    public readonly name: string

    /**
     * Create a backup object
     * @param database - The database name
     */
    constructor(database: string) {
        this.database = database
        this.date = new Date()
        this.name = `${database}-${Backup.formatDate(this.date)}.sql`
    }

    /**
     * Retrieve the data from the database and save it into a file
     */
    async create() {
        /* Create the backup directory if it doesn't exist */
        if (!fs.existsSync(Backup.folder)) {
            fs.mkdirSync(Backup.folder)
        }
        try {
            /* Save the backup */
            await dump({
                connection: {
                    host: process.env.MYSQL_HOST,
                    port: parseInt(process.env.MYSQL_PORT),
                    user: process.env.MYSQL_USER,
                    password: process.env.MYSQL_PASSWORD,
                    database: this.database
                },
                dumpToFile: path.join(Backup.folder, this.name)
            })
            /* Log the backup */
            console.info(`Saved backup for database ${this.database} as ${this.name}`)
        } catch (error) {
            /* Send an error in the console */
            console.error(`Unable to save a backup for database ${this.database}`)
        }
    }

    /**
     * Format a date to save as a file name
     * @param date
     */
    static formatDate(date: Date) {
        return "D" + date.toISOString().substring(0, 19).replace(":", "-")
    }

}