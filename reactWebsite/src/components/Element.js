import React from 'react';
import { Link } from 'react-router-dom';

function Element(props) {
    return (
        <>
        <li className='element'>
            <Link className='element_link' to={props.path}>
                <figure className='element_pic-wrap' data-category={props.label}>
                <img src={props.src}
                className='element_img'
                alt='idk'
                />
                </figure>
                <div className='element_info'>
                    <h5 className='element_text'>{props.text}</h5>
                </div>
            </Link>
        </li>
        </>
        
    );
}

export default Element;
