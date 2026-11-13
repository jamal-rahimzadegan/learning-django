import { apiSvc } from '../svc/api-svc.ts';

type PaymentResult = { url: string };

const handleCheckout = async (eventId: string): Promise<PaymentResult> => {
  return await apiSvc.post<PaymentResult>(
    `/events/create-checkout-session/`,
    { id: eventId },
    { hasVersion: false }
  );
};

export { handleCheckout };
