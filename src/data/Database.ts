import {Connection, createConnection} from "mysql2/promise"
import Backup from "./Backup";

export default class Database {
    /**
     * The database name
     */
    private readonly name: string
    /**
     * The asynchronous init method
     */
    private readonly init: () => void
    /**
     * The MySQL connection object
     */
    private connection: Connection

    /**
     * Connect to the database
     * @param database - The database's name
     * @param init - An asynchronous function called to init the database
     */
    constructor(database: string, init: any) {
        this.name = database;
        this.init = init
    }

    /**
     * Create a connection to the database (can be configured in .env) and initialize the database
     */
    public async connect(): Promise<this> {
        this.connection = await createConnection({
            host: process.env.MYSQL_HOST,
            port: parseInt(process.env.MYSQL_PORT),
            user: process.env.MYSQL_USER,
            password: process.env.MYSQL_PASSWORD,
            database: this.name
        })

        await this.init()
        return this
    }

    /**
     * An equivalent of connection.query()
     * @param sql - The SQL request
     * @param values - The values used to replace '?' in sql scripts
     */
    public async query(sql: string, values?): Promise<any[]> {
        const [rows] = await this.connection.query(sql, values)
        return rows as any[]
    }

    /**
     * Create a backup object to use to save the database
     */
    public backup(): Backup {
        return new Backup(this.name)
    }

}
