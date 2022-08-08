export default class User {
    private readonly id: UserIdentifier

    constructor(id: UserIdentifier) {
        this.id = id
    }

    getIdentifier(): UserIdentifier {
        return this.id
    }

    async exists(): Promise<boolean> {
        return !await this.getIdentity()
    }
    
    async getToken(): Promise<string> {
        const token = await global.data.getTokenByUser(this.id)
        if (token) return token['token_key']
        else return this.regenToken()
    }

    async regenToken(): Promise<string> {
        const token = Math.random().toString(36).substring(2)
        await global.data.setToken(this.id, token)
        return token
    }

    async useToken() {
        await global.data.useToken(this.id)
    }

    async getIdentity(): Promise<UserIdentity> {
        return await global.data.getIdentity(this.id)
    }

    async getPassword(): Promise<string> {
        return await global.data.getPassword(this.id)
    }

    async getPermissions(): Promise<string[]> {
        return await global.data.getPermissions(this.id)
    }

    async hasPermission(permission: string): Promise<boolean> {
        return await global.data.hasPermission(this.id, permission)
    }

    async setPermissions(permissions: string[]) {
        await global.data.setPermissions(this.id, permissions)
    }

    async addPermission(permission: string) {
        await global.data.addPermission(this.id, permission)
    }

    async removePermission(permission: string) {
        await global.data.removePermission(this.id, permission)
    }

    async clearPermissions() {
        await global.data.clearPermissions(this.id)
    }

    async getInvestment(): Promise<number> {
        return await global.data.getInvestment(this.id)
    }

    async setInvestment(fruits: number) {
        await global.data.setInvestment(this.id, fruits)
    }

    async clearInvestment() {
        await global.data.clearInvestment(this.id)
    }

}

export interface UserIdentity {
    id: string
    name: string
    tag: string
}

export type UserIdentifier = string