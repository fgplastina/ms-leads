import { useGetList, SelectInput } from 'react-admin';

const CourseInput = () => {
    const { data, isLoading } = useGetList('courses');
    return (
        <SelectInput 
            source="courses"
            choices={data}
            optionText="name"
            optionValue="code"
            isLoading={isLoading}
        />
    );
}

export default CourseInput;
