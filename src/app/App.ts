import {Express} from "express";
import * as express from 'express';
import * as http from "http";
import * as WebSocket from 'ws';
import BidoyonDatabase from "../data/BidoyonDatabase";
import Users from "../users/Users";
import Sockets from "../sockets/Sockets";

export default class App {
    private express: Express
    private server: http.Server
    private socketServer: WebSocket.Server

    constructor() {
        global.app = this
        this.loadDatabase()
            .then(() => {
                this.loadUsers()
                this.loadSockets()
                this.loadServer()
                this.loadSocketServer()
                this.loadServerEvents()
                this.loadSocketServerEvents()
            })
            .catch((reason) => {
                console.error(reason)
            })
    }

    async loadDatabase() {
        global.data = await new BidoyonDatabase().connect()
    }

    loadUsers() {
        global.users = new Users()
    }

    loadSockets() {
        global.sockets = new Sockets()
    }

    loadServer() {
        this.express = express()
        this.server = this.express.listen(8080)
    }

    loadSocketServer() {
        this.socketServer = new WebSocket.Server({
            noServer: true,
            path: '/events'
        })
    }

    loadServerEvents() {
        this.server.on("upgrade", (request, websocket, head) => {
            this.socketServer.handleUpgrade(request, websocket, head, (socket) => {
                this.socketServer.emit("connection", socket, request);
            });
        });
    }

    loadSocketServerEvents() {
        this.socketServer.on("connection", (socket, request) => {
            socket.on("message", async (data) => {
                const user = global.users.getUserByToken(data.toString())
                if (!user || !await user.exists()) {
                    socket.send('authed')
                    global.sockets.addSocket(socket)

                    socket.on("close", () => {
                        global.sockets.removeSocket(socket)
                    })
                } else {
                    socket.send('notAuthed')
                    socket.close()
                }
            })
        })
    }

}
