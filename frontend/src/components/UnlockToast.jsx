import { AnimatePresence, motion } from "framer-motion";

/**
 * Notificación tipo "sello estampado" que aparece cuando se desbloquea
 * un logro o se completa un desafío. items: [{ id, title, xp_reward }]
 */
export default function UnlockToast({ items, onDismiss }) {
  return (
    <div className="fixed inset-x-4 bottom-4 sm:inset-x-auto sm:bottom-6 sm:right-6 flex flex-col items-stretch sm:items-end gap-2 z-50 pb-[env(safe-area-inset-bottom)]">
      <AnimatePresence>
        {items.map((item) => (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            transition={{ duration: 0.3 }}
            onClick={() => onDismiss(item.id)}
            className="ticket cursor-pointer px-5 py-3 bg-stamp-gold/15 border-stamp-gold/50 flex items-center gap-3 w-full sm:max-w-xs"
          >
            <span className="text-xl" aria-hidden="true">🏅</span>
            <div>
              <p className="text-sm font-medium">{item.title}</p>
              <p className="text-xs font-mono text-stamp-gold">
                +{item.xp_reward} xp
              </p>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
