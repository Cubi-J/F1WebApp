import { useEffect, useState} from "react";
import ReactCountryFlag from "react-country-flag";
import SessionDetailsCard from "./SessionDetailsCard";

export default function NextRaceCard({ race }){

    const [nextRace, setNextRace] = useState([]);
    const [svgContent, setSvgContent] = useState("");
    const [nextRaceSessions, setNextRaceSessions] = useState([]);


    useEffect(() => {
        async function fetchNextRace() {
            try {
                const res = await fetch("http://127.0.0.1:5000/next-race");
                const data = await res.json();
                setNextRace(data);


                const sessionsArray = data.sessions;

                setNextRaceSessions(sessionsArray);

                if (data.Circuit.circuitId) {
                // Fetch the raw SVG string
                    const svgRes = await fetch(
                        `http://127.0.0.1:5000/track-maps/${data.Circuit.circuitId}.svg`
                    );

                    const svgText = await svgRes.text();
                    setSvgContent(svgText);
                }
            } catch (err) {
                console.error("Error loading next race: ", err);
            }
        }
        fetchNextRace();
    }, [])

    const raceSession = nextRaceSessions.find(session => session.key === "Race");
        
    return(
        <div className="w-full mb-6 p-6 bg-white dark:bg-gray-900 rounded-2xl shadow-lg border border-gray-200" id="next-race-card">
            <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                {nextRace.raceName}
            </h2>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-4" id="race-details">
                {nextRace.Circuit?.circuitName} — {nextRace.Circuit?.Location?.locality},{" "}
                {nextRace.Circuit?.Location?.country}
                <span className="mr-2 ml-2">
                    <ReactCountryFlag countryCode={nextRace.countryCode} svg />
                </span>
            </p>
            <p className="text-gray-800 dark:text-gray-200 font-medium">
                {raceSession?.date} — {raceSession?.formattedTime}
            </p>
            <div className="mt-4 w-full h-64 overflow-hidden rounded-lg shadow-md" id="track-map">
                {svgContent ? (
                    <div
                        className="w-full h-full flex items-center justify-center text-gray-900 dark:text-gray-100 
                                    [&>svg]:w-full [&>svg]:h-full [&>svg]:object-contain [&>svg]:max-h-64 [&>path]:fill-gray-800 dark:[&>path]:fill-gray-100"
                        dangerouslySetInnerHTML={{ __html: svgContent }}
                    />
                ) : (
                    <p className="text-gray-500 dark:text-gray-400">Error loading track map</p>
                )}
            </div>

            <div id="sessions">
                {nextRaceSessions.map((session) => (
                    <SessionDetailsCard key={session.key} session={session} />
                ))}
            </div>    
        </div>
    )
}