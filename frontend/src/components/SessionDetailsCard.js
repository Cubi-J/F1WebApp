export default function SessionDetailsCard({ session }){
    return (
        <div className="w-full mb-6 p-6 bg-white dark:bg-gray-900 rounded-2xl shadow-lg border border-gray-200" id="session-details-card">
            <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                {session.name}
            </h2>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-4" id="session-datetime">
                {session.date} — {session.time}
            </p>
        </div>
    )
}