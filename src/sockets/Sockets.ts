import {WebSocket} from "ws";

export default class Sockets {
    private sockets: WebSocket[] = []

    addSocket(socket: WebSocket) {
        this.sockets.push(socket)
    }

    removeSocket(socket: WebSocket) {
        this.sockets.splice(this.sockets.indexOf(socket))
    }

    send(message: string) {
        for (const socket of this.sockets) {
            socket.send(message)
        }
    }

}