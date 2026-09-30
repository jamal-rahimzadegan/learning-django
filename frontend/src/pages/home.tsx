import {useEffect, useState} from "react";
import {getEvents} from "../api/events.ts";

export default function Home() {
    const [events, setEvents] = useState<Event[]>()

    const formatEvents = async () => {
        try {
            const tempEvents = await getEvents()
            setEvents(tempEvents)
        } catch (e) {
            console.error(e)
        }
    }

    useEffect(() => {
        formatEvents()
    }, [])

    return <>
        <h2 className="font-bold font-stretch-125% mb-5 text-gray-700">Events List</h2>
        {events?.map((event, i) => (
            <div key={event.id} className="mb-3">
                <h3 className="font-bold">{i + 1}- {event.title}</h3>
                <p className="ms-6">{event.description}</p>
            </div>
        ))}
    </>
}