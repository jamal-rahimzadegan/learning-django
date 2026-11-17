import { useSearchParams } from 'react-router-dom';
import { skipToken, useQuery, useQueryClient } from '@tanstack/react-query';
import { checkPaymentStatus } from '../../api/payment.ts';

const MAX_ATTEMPTS = 6;
const POLL_INTERVAL_MS = 1500;

export default function PaymentSuccess() {
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get('session_id');
  const queryClient = useQueryClient();
  const queryKey = ['payment-status', sessionId];

  const { data: ticket, error } = useQuery({
    queryKey,
    queryFn: sessionId ? () => checkPaymentStatus(sessionId) : skipToken,
    refetchInterval: (query) =>
      query.state.data?.status === 'pending' &&
      query.state.dataUpdateCount < MAX_ATTEMPTS
        ? POLL_INTERVAL_MS
        : false,
  });

  const timedOut =
    (queryClient.getQueryState(queryKey)?.dataUpdateCount ?? 0) >=
    MAX_ATTEMPTS;

  if (!sessionId) return <div>Missing checkout session ID.</div>;

  if (error) return <div>{error.message}</div>;

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
