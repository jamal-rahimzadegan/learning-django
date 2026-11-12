import { getEvents, type SocialEvent } from '../api/events.ts';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import PageWrapper from '../layout/page-wrapper.tsx';
import { Button } from '../components/shared/button.tsx';

export default function EventDetails() {
  const { id } = useParams();
  const navigate = useNavigate();

  const { data: event, isFetching } = useQuery({
    enabled: !!id,
    queryKey: ['event', id],
    queryFn: () => getEvents<SocialEvent>(id),
  });

  const price = event?.price || 0;

  const goToPayment = () => {
    //TODO: call the backend api to prepare payment
    // alert(`pay ${price} ${event.id}`);
    // navigate('/login', {});
  };

  return (
    <PageWrapper isEmpty={!event?.id} isLoading={isFetching}>
      <div key={event?.id} className="mb-3">
        <h3 className="font-bold mt-5">{event?.title}</h3>
        <p className="mt-2">{event?.description}</p>
      </div>
      {price > 0 ? <Button onClick={goToPayment}>Buy {price} €</Button> : null}
    </PageWrapper>
  );
}
