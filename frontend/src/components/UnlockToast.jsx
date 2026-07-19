import { AnimatePresence, motion } from "framer-motion";

/**
 * Notificación tipo "sello estampado" que aparece cuando se desbloquea
 * un logro o se completa un desafío. items: [{ id, title, xp_reward }]
 */
export default function UnlockToast({ items, onDismiss }) {
  return (
    <div className="fixed bottom-6 right-6 flex flex-col gap-2 z-50">
      <AnimatePresence>
        {items.map((item) => (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            transition={{ duration: 0.3 }}
            onClick={() => onDismiss(item.id)}
            className="ticket cursor-pointer px-5 py-3 bg-stamp-gold/15 border-stamp-gold/50 flex items-center gap-3 max-w-xs"
          >
            <span className="text-xl">🏅</span>
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
