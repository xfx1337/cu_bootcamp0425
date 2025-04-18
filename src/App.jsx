import React from 'react';
import { BrowserRouter as Router, Link } from 'react-router-dom';
import { 
  HiOutlineLightBulb, 
  HiOutlineAcademicCap, 
  HiOutlineChatAlt2, 
  HiOutlineClipboardList 
} from "react-icons/hi";
import { motion } from 'framer-motion';

const App = () => {
  return (
    <Router>
      <div className="bg-gradient-to-b from-[#0d0d0d] to-[#1a1a1a] min-h-screen text-white">
        {/* Шапка с градиентом */}


<header className="relative pt-20 pb-32 overflow-hidden ">
  {/* Анимированный фон с частицами */}

  {/* Основной контент */}
  <div className="container mx-auto relative z-10 text-center">
    <motion.h1 
      className="text-6xl md:text-8xl  font-black text-[#fff] mb-8  "
      initial={{ opacity: 0, y: -50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, delay: 0.2 }}
    >
      Выбираем вуз<br/>без страха
    </motion.h1>
    
    <motion.p 
      className="text-xl md:text-3xl mb-12 text-gray-300 font-medium"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.4 }}
    >
      Ваш персональный гид в мире образования
    </motion.p>

    {/* Кнопка с эффектом */}
    <motion.button 
      className="relative bg-[#6E7BF2]  text-white py-5 px-14 rounded-full 
                 font-semibold hover:bg-[#2437EC] transition-all duration-300 overflow-hidden group"
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.98 }}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5, delay: 0.6 }}
    >
      <a href='https://t.me/online_postupishka_bot'  className="relative z-10">Начать сейчас</a>
      <div className="absolute inset-0 bg-white/10 rounded-full transition-transform duration-300 
                     group-hover:scale-150 group-hover:opacity-0" />
      <div className="absolute inset-0 bg-gradient-to-r from-purple-400 to-purple-600 
                     rounded-full opacity-0 group-hover:opacity-20 transition-opacity duration-300" />
    </motion.button>
  </div>
</header>

        {/* Улучшенный раздел возможностей */}
        <section className="container mx-auto mt-20 px-4 mb-40">
  {/* Заголовок с анимацией */}
  <motion.h2 
    className="text-4xl md:text-5xl font-bold mb-12 text-center text-[#fff]"
    initial={{ opacity: 0, y: -50 }}
    whileInView={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.8 }}
  >
    Почему выбирают нас?
  </motion.h2>
  
  {/* Блоки возможностей */}
  <div className="grid px-5 grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
    {[...Array(4)].map((_, i) => (
      <motion.div 
        key={i}
        className="relative p-8 bg-gradient-to-b from-[#2437EC]/20 to-[#6E7BF2]/10 rounded-3xl overflow-hidden"
        initial={{ y: 50, opacity: 0 }}
        whileInView={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, delay: i * 0.2 }}
        whileHover={{ scale: 1.05 }}
      >
        {/* Анимированный градиентный оверлей */}
        <div className="absolute inset-0 bg-gradient-radial from-[#2437EC]/40 via-transparent to-transparent rounded-3xl blur-xl transition-opacity duration-500 group-hover:opacity-100 opacity-50" />
        
        <div className="relative z-10 space-y-4">
          {/* Иконки с анимацией */}
          {i === 0 && (
            <motion.div 
              className="w-16 h-16 mx-auto text-[#7d88f3] mb-4"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 100 }}
            >
              <HiOutlineAcademicCap className="w-full h-full" />
            </motion.div>
          )}
          {i === 1 && (
            <motion.div 
              className="w-16 h-16 mx-auto text-[#7d88f3] mb-4"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 100, delay: 0.2 }}
            >
              <HiOutlineLightBulb className="w-full h-full" />
            </motion.div>
          )}
          {i === 2 && (
            <motion.div 
              className="w-16 h-16 mx-auto text-[#7d88f3] mb-4"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 100, delay: 0.4 }}
            >
              <HiOutlineChatAlt2 className="w-full h-full" />
            </motion.div>
          )}
          {i === 3 && (
            <motion.div 
              className="w-16 h-16 mx-auto text-[#7d88f3] mb-4"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 100, delay: 0.6 }}
            >
              <HiOutlineClipboardList className="w-full h-full" />
            </motion.div>
          )}
          
          {/* Заголовки карточек */}
          <motion.h3 
            className="text-xl font-semibold text-[#fff] text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 + (i * 0.1) }}
          >
            {["Подготовка к ЕГЭ", "Профориентация", "Психологическая поддержка", "План поступления"][i]}
          </motion.h3>
          
          {/* Описания карточек */}
          <motion.p 
            className="text-gray-400 text-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 + (i * 0.1) }}
          >
            {[
              "Персональные графики и пробные тесты",
              "Тесты и анализ ваших сильных сторон",
              "Ежедневные советы и чат с психологом",
              "Пошаговая инструкция от выбора до зачисления"
            ][i]}
          </motion.p>
        </div>
      </motion.div>
    ))}
  </div>
</section>

        {/* Интерактивный мобильный макет */}
        <div className="relative mb-40 overflow-hidden">
  {/* Анимированный фон с частицами */}
  <div className="absolute inset-0 z-0">
    {[...Array(10)].map((_, i) => (
      <motion.div
        key={i}
        className="absolute w-6 h-6 rounded-full bg-[#2437EC]/30 blur-xl"
        initial={{ x: Math.random() * window.innerWidth, y: Math.random() * window.innerHeight }}
        animate={{
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight,
        }}
        transition={{
          duration: Math.random() * 10 + 5,
          repeat: Infinity,
          repeatType: 'reverse',
          ease: 'linear'
        }}
      />
    ))}
  </div>
  
  {/* Основной контент */}
  <div className="container mx-auto px-4  relative z-10">
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
      {/* Левая часть (текстовая) */}
      <motion.div 
        className="ml-15 mr-15 order-2 lg:order-1"
        initial={{ opacity: 0, x: -50 }}
        whileInView={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8 }}
      >
        {/* Заголовок с анимацией градиента */}
        <motion.h2 
          className="text-4xl md:text-5xl font-bold mb-6 text-white"
          initial={{ backgroundPosition: '0% 50%' }}
          animate={{ backgroundPosition: '100% 50%' }}
          transition={{ duration: 5, repeat: Infinity, ease: 'linear' }}
        >
          Как это работает?
        </motion.h2>
        
        {/* Описание */}
        <motion.p 
          className="text-white text-lg mb-8"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          Бот анализирует ваши интересы, страхи и текущий уровень подготовки, создавая индивидуальную траекторию
        </motion.p>
        
        {/* Список возможностей */}
        <ul className="space-y-4 text-white">
          {[...Array(6)].map((item, i) => (
            <motion.li 
              key={i}
              className="flex items-center space-x-3"
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.4 + i * 0.2 }}
            >
              <span className="w-2 h-2 bg-white rounded-full" />
              <span>
                {[
                  "Поддержка 24/7",
                  "Помощь в выборе специальности",
                  "Рекомендации по вузам",
                  "Анализ пробелов в знаниях",
                  "Напоминания о занятиях",
                  "Ежедневная проверка знаний "

                  
                ][i]}
              </span>
            </motion.li>
          ))}
        </ul>
      </motion.div>
      
      {/* Правая часть (изображение) */}
      <motion.div 
        className="order-1 lg:order-2 flex justify-center"
        initial={{ opacity: 0, x: 50 }}
        whileInView={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8 }}
      >
        <img 
          src="/image-Photoroom (10).png" 
          alt="Telegram бот интерфейс"
          className="w-[60%] rounded-3xl  transition-transform duration-500"
        />
      </motion.div>
    </div>
  </div>
</div>

        {/* Мощный CTA с градиентом */}
        <section className="relative pb-20 overflow-hidden">
  {/* Анимированный фон с частицами */}
  
  {/* Основной контент */}
  <motion.div 
    className="container mx-auto text-center relative z-10"
    initial={{ opacity: 0, y: 50 }}
    whileInView={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.8 }}
  >
    {/* Заголовок с анимацией градиента */}
    <motion.h2 
      className="text-4xl md:text-6xl font-bold mb-6 text-[#fff]"
      initial={{ backgroundPosition: '0% 50%' }}
      animate={{ backgroundPosition: '100% 50%' }}
      transition={{ duration: 5, repeat: Infinity, ease: 'linear' }}
    >
      Готовы начать?
    </motion.h2>
    
    {/* Подзаголовок */}
    <motion.p 
      className="text-gray-400 text-lg mb-8"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      transition={{ duration: 0.6, delay: 0.4 }}
    >
      Станьте тем, кто будет уверен в своем будущем
    </motion.p>
    
    {/* Кнопка с эффектами */}
    <motion.button 
      className="relative   bg-[#6E7BF2] hover:bg-[#3d37f0] transition-all text-white py-4 px-12 rounded-full font-bold overflow-hidden cursor-pointer"
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.98 }}
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      transition={{ duration: 0.5, delay: 0.6 }}
      href='https://t.me/online_postupishka_bot' 

    >
      <a href='https://t.me/online_postupishka_bot'  className="relative z-10">Начать бесплатно</a>
      

    </motion.button>
  </motion.div>
</section>
      
      </div>
    </Router>
  );
};

export default App;