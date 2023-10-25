import { useGetList, SelectInput } from 'react-admin';

const CareerInput = () => {
    const { data, isLoading } = useGetList('careers');
    return (
        <SelectInput 
            source="careers"
            choices={data}
            optionText="name"
            optionValue="code"
            isLoading={isLoading}
        />
    );
}

export default CareerInput;
