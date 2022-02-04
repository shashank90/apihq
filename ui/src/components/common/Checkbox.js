export default function Checkbox(props) {
  const name = props.name;
  const label = props.label;
  const checked = props.checked;
  const onChange = props.onChange;
  console.log("Checkbox: ", name, checked);

  return (
    <div>
      <input
        type="checkbox"
        name={name}
        checked={checked}
        onChange={onChange}
      />
      <label>{label}</label>
    </div>
  );
}
