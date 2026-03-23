import React from 'react';

const InfoModal = ({ isOpen, onClose, isWelcome = false }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[2000] flex items-center justify-center bg-black bg-opacity-50 p-4 transition-opacity backdrop-blur-sm">
      <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full overflow-hidden flex flex-col max-h-[90vh] animate-in fade-in zoom-in duration-300">
        {/* Header */}
        <div className="bg-emerald-700 text-white p-6 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            {/* Simple Tree Logo */}
            <svg className="w-8 h-8 fill-current text-emerald-100" viewBox="0 0 24 24">
              <path d="M12 2L4.5 20.29L5.21 21L12 18L18.79 21L19.5 20.29L12 2Z" />
            </svg>
            <h1 className="text-2xl font-bold tracking-tight leading-none">Madrid, de árbol en árbol</h1>
          </div>
          <button
            onClick={onClose}
            className="text-emerald-100 hover:text-white transition-colors p-1"
            title="Cerrar"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="p-8 overflow-y-auto space-y-8">
          {isWelcome && (
            <section className="text-center pb-6 border-b border-emerald-50">
              <h2 className="text-xl font-semibold text-emerald-800 mb-2">¡Bienvenido a «Madrid de Árbol en Árbol»!</h2>
              <p className="text-gray-600 leading-relaxed">
                Recorre Madrid de una manera diferente: saltando de árbol en árbol (o, si no eres una ardilla, a la sombra de nuestros amigos los árboles).
              </p>
            </section>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <section>
              <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
                <svg className="w-5 h-5 mr-2 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Instrucciones
              </h3>
              <ul className="text-gray-600 space-y-3">
                <li className="flex items-start">
                  <span className="inline-flex items-center justify-center bg-emerald-100 text-emerald-800 rounded-full w-5 h-5 text-xs font-bold mr-2 mt-0.5 shrink-0">1</span>
                  <span>Haz <strong>clic</strong> en el mapa para marcar el punto de inicio <strong>(A)</strong>.</span>
                </li>
                <li className="flex items-start">
                  <span className="inline-flex items-center justify-center bg-emerald-100 text-emerald-800 rounded-full w-5 h-5 text-xs font-bold mr-2 mt-0.5 shrink-0">2</span>
                  <span>Haz un <strong>segundo clic</strong> para marcar el destino final <strong>(B)</strong>.</span>
                </li>
                <li className="flex items-start">
                  <span className="inline-flex items-center justify-center bg-emerald-100 text-emerald-800 rounded-full w-5 h-5 text-xs font-bold mr-2 mt-0.5 shrink-0">3</span>
                  <span>Un <strong>tercer clic</strong> reiniciará el mapa para una nueva búsqueda.</span>
                </li>
              </ul>
            </section>

            <section>
              <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
                <svg className="w-5 h-5 mr-2 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
                Acerca del proyecto
              </h3>
              <p className="text-gray-600 leading-relaxed text-sm">
                Se dice que en época de los romanos, una ardilla podía atravesar Hispania saltando de árbol en árbol.
                ¿Podría esa ardilla cruzar el Madrid de hoy de la misma manera? Usando datos abiertos del Ayuntamiento de Madrid, esta aplicación te permitirá navegar la villa de una manera diferente.
              </p>
            </section>
          </div>

          <div className="pt-6 border-t border-gray-100 flex flex-col sm:flex-row justify-between items-center text-xs text-gray-400 gap-4">
            <div className="flex flex-col text-center sm:text-left">
              <span>© 2026 Madrid, de árbol en árbol. Datos de OSM y del Ayuntamiento de Madrid.</span>
              <span className="mt-1 text-emerald-600/60 font-medium">Este proyecto no utiliza <i>cookies</i> ni realiza ningún tipo de rastreo de usuarios.</span>
            </div>
            <button
              onClick={onClose}
              className="px-8 py-2.5 bg-emerald-600 text-white rounded-lg font-semibold hover:bg-emerald-700 transition-colors shadow-lg active:scale-95 transform"
            >
              Comenzar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InfoModal;
