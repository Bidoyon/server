import App from "./app/App";
import BidoyonDatabase from "./data/BidoyonDatabase";
import Users from "./users/Users";
import Sockets from "./sockets/Sockets";

declare global {
    var app: App
    var users: Users
    var data: BidoyonDatabase
    var sockets: Sockets
}
