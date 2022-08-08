import User, {UserIdentifier} from "./User";

export default class Users {
    private users: { [key: string]: User } = {}

    getUserByID(id: UserIdentifier) {
        if (id in this.users) {
            return this.users[id]
        }
        const user = new User(id)
        this.users[id] = user
        return user
    }

    getUserByToken(tokenKey: string) {
        const token = global.data.getTokenByKey(tokenKey)
        if (token) {
            return this.getUserByID(token['user'])
        }
        return undefined
    }

}
