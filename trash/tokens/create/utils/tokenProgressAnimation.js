export class ProgressAnimator {
    constructor() {
        this.interval = null;
    }

    startAnimation(setProgress, steps = [15, 35, 55, 75, 90], delay = 400) {
        this.stopAnimation();
        
        let stepIndex = 0;
        this.interval = setInterval(() => {
            if (stepIndex < steps.length) {
                setProgress(steps[stepIndex]);
                stepIndex++;
            }
        }, delay);
    }

    async completeTo100(setProgress, finalSteps = [95, 98, 100], delay = 150) {
        this.stopAnimation();
        
        return new Promise(resolve => {
            let stepIndex = 0;
            
            const finalInterval = setInterval(() => {
                if (stepIndex < finalSteps.length) {
                    setProgress(finalSteps[stepIndex]);
                    stepIndex++;
                } else {
                    clearInterval(finalInterval);
                    setTimeout(resolve, 200);
                }
            }, delay);
        });
    }

    /**
     * Остановка анимации
     */
    stopAnimation() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    }

    /**
     * Сброс прогресса
     * @param {Function} setProgress - функция обновления прогресса
     */
    reset(setProgress) {
        this.stopAnimation();
        setProgress(0);
    }
}

export function useProgressAnimation() {
    const animator = new ProgressAnimator();
    
    return {
        /**
         * Запуск анимации
         * @param {Function} setProgress - функция обновления прогресса
         */
        startProgress(setProgress) {
            animator.startAnimation(setProgress);
        },

        /**
         * Завершение до 100%
         * @param {Function} setProgress - функция обновления прогресса
         */
        async completeProgress(setProgress) {
            await animator.completeTo100(setProgress);
        },

        /**
         * Остановка анимации
         */
        stopProgress() {
            animator.stopAnimation();
        },

        /**
         * Сброс прогресса
         * @param {Function} setProgress - функция обновления прогресса
         */
        resetProgress(setProgress) {
            animator.reset(setProgress);
        },

        /**
         * Очистка при уничтожении компонента
         */
        destroy() {
            animator.stopAnimation();
        }
    };
}