import { useCallback, useState } from 'react';

// custom hook for input fields. Needs a validator to validate input.
const useFile = (validateValue) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [isTouched, setIsTouched] = useState(false);

    const valueIsValid = validateValue(selectedFile);
    const hasError = !valueIsValid && isTouched;

    // handle change of value
    const valueChangeHandler = (file) => {
        setSelectedFile(file);
    };

    // handle lost focus on input field
    const inputBlurHandler = useCallback((event) => {
        setIsTouched(true);
    }, []);

    return {
        value: selectedFile,
        valueIsValid,
        hasError,
        valueChangeHandler,
        inputBlurHandler
    };
};

export default useFile;
