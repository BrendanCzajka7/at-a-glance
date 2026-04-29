import type { NasaNeo } from "../../types/dashboard";
import { NasaNeoMini } from "./NasaNeoMini";

type Props = {
  neos: NasaNeo[];
};

export function NasaNeoToday({ neos }: Props) {
  return (
    <section>
      <h3>Near-Earth Objects Today</h3>
      <NasaNeoMini neos={neos} />
    </section>
  );
}