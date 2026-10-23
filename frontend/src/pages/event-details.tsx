import { getEvents, type SocialEvent } from '../api/events.ts';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import PageWrapper from '../layout/page-wrapper.tsx';

export default function EventDetails() {
  const { id } = useParams();

  const { data: event, isFetching } = useQuery({
    enabled: !!id,
    queryKey: ['event', id],
    queryFn: () => getEvents<SocialEvent>(id),
  });

  return (
    <PageWrapper isEmpty={!event?.id} isLoading={isFetching}>
      <div key={event?.id} className="mb-3">
        <h3 className="font-bold mt-5">{event?.title}</h3>
        <p className="mt-2">{event?.description}</p>
      </div>
    </PageWrapper>
  );
}
