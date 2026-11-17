import { apiSvc } from '../svc/api-svc.ts';

type PaymentResult = { url: string };

export type TicketStatusResponse = {
  ticket_id: string;
  status: 'pending' | 'paid' | 'refunded';
  event_title: string;
};

async function handleCheckout(eventId: string): Promise<PaymentResult> {
  return await apiSvc.post<PaymentResult>(
    `/events/create-checkout-session/`,
    { id: eventId },
    { hasVersion: false },
  );
}

async function checkPaymentStatus(
  sessionId: string,
): Promise<TicketStatusResponse> {
  return await apiSvc.get<TicketStatusResponse>(
    `/events/checkout-status/${sessionId}/`,
    { hasVersion: false },
  );
}





export { handleCheckout, checkPaymentStatus };
