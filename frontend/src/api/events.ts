import {apiSvc} from "../svc/api-svc.ts";

interface Event {
    title: string;
    description: string | null;
    organizer_id: number;
    status: string;
    created_at: string;
    location: string | null;
    start_time: string | null;
    price: number;
    capacity: number | null;
    id:string
}


const getEvents = async () => {
    return await apiSvc.get<Event[]>('/events')
}

export type {
    Event
}

export {
    getEvents
}