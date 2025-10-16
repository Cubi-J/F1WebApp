import { useEffect, useState } from "react";
import DriverCard from "./DriverCard";

export default function DriversGrid() {
  const [driversByTeam, setDriversByTeam] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchDrivers() {
      try {
        const res = await fetch("http://127.0.0.1:5000/drivers");
        const data = await res.json();
        if (data.error) {
          setError(data.error);
          setDriversByTeam([]);
        } else {
          setDriversByTeam(data);
        }
      } catch (err) {
        console.error("Error loading drivers:", err);
      };
    };
      fetchDrivers();
    }, []);

  return (
    <div className="grid gap-10 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-6">
      {error ? (
        <p className = "col-span-full bg-red-500">{error}</p>
      ) : (
        driversByTeam.map(team =>
          team.drivers.map(driver => (
            <DriverCard key={driver.driver_number} driver={driver} />
          ))
        )
      )}
    </div>
  );
}
