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

interface EventsDto<T> {
  count: number;
  next: string;
  previous: string;
  results: T;
}

async function getEvents<T>({ page = 1 }: { page?: number } = {}) {
  return await apiSvc.get<EventsDto<T>>(`/events/?page=${page}`);
}

async function getEventById<T>(id: string = '') {
  return await apiSvc.get<T>(`/events/${id}/`);
}

export type { SocialEvent };

export { getEvents, getEventById };
