import { apiSvc } from '../svc/api-svc.ts';

interface SocialEvent {
  title: string;
  description: string | null;
  organizer_id: number;
  status: string;
  created_at: string;
  location: string | null;
  start_time: string | null;
  price: number;
  capacity: number | null;
  id: string;
}

const getEvents = async <T>(id?: string) => {
  return await apiSvc.get<T>(`/events/${id ?? ''}`);
};

export type { SocialEvent };

export { getEvents };
