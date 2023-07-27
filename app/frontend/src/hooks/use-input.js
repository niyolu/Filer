import { useCallback, useState } from 'react';

// custom hook for input fields. Needs a validator to validate input.
const useInput = (validateValue, defaultValue = '') => {
    const [enteredValue, setEnteredValue] = useState(defaultValue);
    const [isTouched, setIsTouched] = useState(false);

    const valueIsValid = validateValue(enteredValue);
    const hasError = !valueIsValid && isTouched;

    // handle change of value
    const valueChangeHandler = (event) => {
        setEnteredValue(event.target.value);
    };

    // handle lost focus on input field
    const inputBlurHandler = useCallback((event) => {
        setIsTouched(true);
    }, []);

    return {
        value: enteredValue,
        valueIsValid,
        hasError,
        valueChangeHandler,
        inputBlurHandler
    };
};

export default useInput;
