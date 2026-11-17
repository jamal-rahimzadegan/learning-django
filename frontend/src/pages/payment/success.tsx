import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';

type TicketStatusResponse = {
  ticket_id: string;
  status: 'pending' | 'paid' | 'refunded';
  event_title: string;
};

export default function PaymentSuccess() {
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get('session_id');

  const [ticket, setTicket] = useState<TicketStatusResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [timedOut, setTimedOut] = useState(false);

  useEffect(() => {
    if (!sessionId) {
      setError('Missing checkout session ID.');
      return;
    }

    let isCancelled = false;
    let attempts = 0;
    const maxAttempts = 6;

    const checkStatus = async () => {
      try {
        const res = await fetch(
          `${import.meta.env.VITE_API_BASE_URL}/events/checkout-status/${sessionId}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          }
        );

        if (!res.ok) {
          throw new Error('Could not verify ticket status.');
        }

        const data: TicketStatusResponse = await res.json();
        if (isCancelled) return;

        setTicket(data);

        if (data.status === 'pending') {
          attempts += 1;
          if (attempts < maxAttempts) {
            setTimeout(checkStatus, 1500);
          } else {
            setTimedOut(true);
          }
        }
      } catch (err) {
        if (!isCancelled) {
          setError(err instanceof Error ? err.message : 'Unexpected error.');
        }
      }
    };

    checkStatus();

    return () => {
      isCancelled = true;
    };
  }, [sessionId]);

  if (error) return <div>{error}</div>;

  if (!ticket || (ticket.status === 'pending' && !timedOut)) {
    return <div>Confirming your payment with Stripe...</div>;
  }

  if (timedOut && ticket.status === 'pending') {
    return (
      <div>
        Payment is still processing. Your ticket will appear in your account
        shortly.
      </div>
    );
  }

  return (
    <div>
      <h1>Payment Successful</h1>
      <p>Event: {ticket.event_title}</p>
      <p>Ticket ID: {ticket.ticket_id}</p>
    </div>
  );
}
