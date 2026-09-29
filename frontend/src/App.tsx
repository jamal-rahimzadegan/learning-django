import './App.css'
import {Fragment, useEffect, useState} from "react";
import {type Event, getEvents} from "./api/events.ts";

export default function App() {
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

    return (
        <>
            <h1>Social event app frontend</h1>

        {events?.map((event) => (
            <div key={event.id} style={{width:'100%',textAlign:'left',gap:5,display:"flex",flexDirection:'column'}}>
                <h2>{event.title}</h2>
                <p>{event.description}</p>
                <hr width={'100%'}/>
            </div>
        ))}
        </>
    )
}

