import Database from "./Database";
import {
    MAX_CHARACTERS_IN_CONTAINER_ID,
    MAX_CHARACTERS_IN_PERMISSION,
    MAX_CHARACTERS_IN_TOKEN,
    MAX_CHARACTERS_IN_USER_ID,
    MAX_CHARACTERS_IN_USER_NAME,
    MAX_CHARACTERS_IN_USER_PASSWORD,
    MAX_CHARACTERS_IN_USER_TAG
} from "../config";
import {UserIdentifier, UserIdentity} from "../users/User";

export default class BidoyonDatabase extends Database {

    constructor() {
        super("bidoyon", async () => {
            await this.query("CREATE TABLE IF NOT EXISTS tokens (user VARCHAR(?), token_key VARCHAR(?), last_usage BIGINT UNSIGNED)", [MAX_CHARACTERS_IN_USER_ID, MAX_CHARACTERS_IN_TOKEN])
            await this.query("CREATE TABLE IF NOT EXISTS users (id VARCHAR(?) PRIMARY KEY, name VARCHAR(?), tag VARCHAR(?), password VARCHAR(?))", [MAX_CHARACTERS_IN_USER_ID, MAX_CHARACTERS_IN_USER_NAME, MAX_CHARACTERS_IN_USER_TAG, MAX_CHARACTERS_IN_USER_PASSWORD])
            await this.query("CREATE TABLE IF NOT EXISTS permissions (user VARCHAR(?), permission VARCHAR(?), PRIMARY KEY (user, permission))", [MAX_CHARACTERS_IN_USER_ID, MAX_CHARACTERS_IN_PERMISSION])
            await this.query("CREATE TABLE IF NOT EXISTS investments (user VARCHAR(?) PRIMARY KEY, fruits INTEGER UNSIGNED)", [MAX_CHARACTERS_IN_USER_ID])
            await this.query("CREATE TABLE IF NOT EXISTS squeezes (id INTEGER PRIMARY KEY, fruits INTEGER UNSIGNED, juice INTEGER UNSIGNED)", [MAX_CHARACTERS_IN_USER_ID])
            await this.query("CREATE TABLE IF NOT EXISTS containers (id VARCHAR(?) PRIMARY KEY, capacity INTEGER UNSIGNED, filling INTEGER UNSIGNED, owner VARCHAR(?))", [MAX_CHARACTERS_IN_CONTAINER_ID, MAX_CHARACTERS_IN_USER_ID])
        });
    }

    async getTokenByKey(tokenKey: string) {
        const values = await this.query("SELECT user, token_key, last_usage FROM tokens WHERE token_key=?", [tokenKey])
        if (!values[0] || Date.now() - values[0]['last_usage'] > 604800000) {
            return undefined
        }
        return values[0]
    }

    async getTokenByUser(user: string) {
        const values = await this.query("SELECT user, token_key, last_usage FROM tokens WHERE user=?", [user])
        if (!values[0] || Date.now() - values[0]['last_usage'] > 604800000) {
            return undefined
        }
        return values[0]
    }

    async setToken(user: UserIdentifier, tokenKey: string) {
        await this.query("REPLACE INTO tokens (user, token_key, last_usage) VALUES (?, ?, ?)", [user, tokenKey, Date.now()])
    }

    async useToken(tokenKey: string) {
        await this.query("UPDATE tokens SET last_usage=? WHERE token_key=?", [Date.now(), tokenKey])
    }

    async getIdentity(id: UserIdentifier): Promise<UserIdentity> {
        const values = await this.query("SELECT id, name, tag FROM users WHERE id=?", [id])
        return values[0]
    }

    async addIdentity(identity: UserIdentity) {
        await this.query("REPLACE INTO users (id, name, tag) VALUES (?, ?, ?)", [identity.id, identity.name, identity.tag])
    }

    async removeIdentity(id: UserIdentifier) {
        await this.query("DELETE FROM users WHERE id=?", [id])
    }

    async getPassword(id: UserIdentifier): Promise<string> {
        const values = await this.query("SELECT password FROM users WHERE id=?", [id])
        return values[0] ? values[0]['password'] : undefined
    }

    async setPassword(id: UserIdentifier, password: string) {
        await this.query("UPDATE users SET password=? WHERE id=?", [password, id])
    }

    async getPermissions(id: UserIdentifier): Promise<string[]> {
        const permissions: string[] = []
        const values = await this.query("SELECT permission FROM permissions WHERE user=?", [id])
        for (const value of values) {
            permissions.push(value['permission'])
        }
        return permissions
    }

    async hasPermission(id: UserIdentifier, permission: string) {
        const values = await this.query("SELECT permission FROM permissions WHERE user=? AND permission=?", [id, permission])
        return values.length > 0
    }

    async setPermissions(id: UserIdentifier, permissions: string[]) {
        await this.clearPermissions(id)
        for (const permission of permissions) {
            await this.addPermission(id, permission)
        }
    }

    async clearPermissions(id: UserIdentifier) {
        await this.query("DELETE FROM permissions WHERE user=?", [id])
    }

    async addPermission(id: UserIdentifier, permission: string) {
        await this.query("REPLACE INTO permissions (user, permission) VALUES (?, ?)", [id, permission])
    }

    async removePermission(id: UserIdentifier, permission: string) {
        await this.query("DELETE FROM permissions WHERE user=? AND permission=?", [id, permission])
    }

    async getInvestment(id: UserIdentifier): Promise<number> {
        const values = await this.query("SELECT fruits FROM investments WHERE user=?", [id])
        return values[0] ? values[0]['fruits'] : 0
    }

    async setInvestment(id: UserIdentifier, fruits: number) {
        await this.query("REPLACE INTO investments (user, fruits) VALUES (?, ?)", [id, fruits])
    }

    async clearInvestment(id: UserIdentifier) {
        await this.query("DELETE FROM investments WHERE user=?", [id])
    }

}